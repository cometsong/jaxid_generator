#!/usr/bin/env bash

#-----------------------------------------------------------------------#
#  Backs up data from 'default' database as an indented JSON document,  #
#  then gzips it.                                                       #
#-----------------------------------------------------------------------#


#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ Functional! ~~~~~
function get_datestamp () { #{{{ ### from cometsong_util_functions.sh ###
    FORMAT=${*:-"%Y-%m-%d %H:%M:%S"}
    DATESTAMP=$(date +"$FORMAT")
    echo $DATESTAMP
} #}}}
function get_datestamp_ymd () { #{{{ ### from cometsong_util_functions.sh ###
    FORMAT="%Y%m%d"
    echo $(get_datestamp $FORMAT)
} #}}}

### from utils.sh ###
# print: echoes all args to stdout
function print() { printf '%b\n' "$@"; }
# err: echoes all args to stderr
function err()   { print "$*" >&2; }
# debug: calls `err`
function debug() { err "$@"; }
# die: sends all args to `err` then exits >0
function die()   { err "$@" && exit 11; }

function exclusion_args() { #{{{
    # prepend "-e " to each element in passed string
    List=( $@ )
    Prepended=""
    for element in ${List[@]} ; do
        Prepended+="-e $element "
    done
    echo "$Prepended"
} #}}}

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ Variables ~~~~~
App=${1:-"jaxid_dev"}

Today=$(get_datestamp_ymd)

Format="json"
DjangoAppPath="/var/www/apps/${App}"
BackupFile="${DjangoAppPath}/backups/${Today}.db.${App}.${Format}"

#Exclusions=$(exclusion_args "sessions contenttypes auth admin.logentry")
Exclusions=$(exclusion_args "sessions contenttypes auth")

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ Back Me Up! Dump Me Out! ~~~~~

print "Beginning data dump of default django database."

[[ -d ${DjangoAppPath} ]] && cd ${DjangoAppPath} && . ./bin/activate
if [[ $? == 0 ]]; then
    #--natural-foreign \
manage.py dumpdata \
    --format $Format \
    --natural-primary \
    --indent 4 \
    ${Exclusions} \
    -o ${BackupFile} \
    \
    && gzip -v ${BackupFile}
fi

print "Database dump now at: ${BackupFile}.gz"

# vim: ft=sh fdm=marker:
