#!/usr/bin/env bash

USAGE="
#--------------------------------------------------------------#
#   Restore data in the development instance of the database   #
#   from the specified backup of the production or other db.   #
#--------------------------------------------------------------#
"

### Fun ###
print() { printf "%b\n" "$@"; }
debug() { print "Debug: " "$@" >&2; }
exitd() { debug "$@" && exit 11; }
exit1() { print "$@" && exit 1; }

### Trapped ###
finishUp() { print "Finished."; }
trap finishUp EXIT

### Vars ###
backup_file=${1?"$USAGE    Please tell me which backup file to get data from..."}
db_name=jaxid_db_devel
app=id_generate
settings=generator.settings.dev
password=$(read -sp 'Enter password: ' pw; echo $pw) && echo # append EOL
#exitd "pass: '$password'"

tables=( $(mysql -p${password} ${db_name} <<< 'show tables;' | grep ^${app};) )
#debug "${tables[@]}"

truncates=''
for tbl in "${tables[@]}"; do truncates+="TRUNCATE \`${tbl}\`; " ; done
#exitd "truncates: '$truncates'"

flush_sql=" BEGIN; SET FOREIGN_KEY_CHECKS = 0; ${truncates} SET FOREIGN_KEY_CHECKS = 1; COMMIT;"
#exitd "sql '${flush_sql}'"

print "Flushing all data ${app} from the ${db_name} database"
mysql -p${password} $db_name <<< $flush_sql
flushed=$?
#exitd "flushed: '$flushed'"

if [[ $flushed -eq 0 ]]; then
    print "Loading backed up data into the '${app}' of the db '${db_name}'."
    echo "manage.py loaddata -v3 --settings ${settings} --database default --app ${app} ${backup_file}"
    manage.py loaddata -v3 --settings ${settings} --database default --app ${app} ${backup_file}
    loaded=$?
    #exitd "loaded: '$loaded'"
else 
    exit1 "DB flushing had errors."
fi

if [[ $loaded -eq 0 ]]; then
    print "Data reloaded."
else 
    exit1 "Loading had errors."
fi
