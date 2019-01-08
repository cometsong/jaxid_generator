#!/usr/bin/env bash

#-----------------------------------------------------------------------#
#  Backs up data from 'default' database as an indented JSON document,  #
#  then gzips it.                                                       #
#-----------------------------------------------------------------------#


#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ Functional! ~~~~~
get_datestamp () { #{{{ ### from cometsong_util_functions.sh ###
    FORMAT=${*:-"%Y-%m-%d %H:%M:%S"}
    DATESTAMP=$(date +"$FORMAT")
    echo $DATESTAMP
} #}}}
get_datestamp_ymd () { #{{{ ### from cometsong_util_functions.sh ###
    FORMAT="%Y%m%d"
    echo $(get_datestamp $FORMAT)
} #}}}

### print/err/die funcs from cometsong_util_functions.sh ### #{{{
# print: echoes all args to stdout
    print() { printf '%b\n' "$@"; }
# err: echoes all args to stderr
    err()   { print "$*" >&2; }
# debug: calls `err`
    debug() { err "$@"; }
# die: sends all args to `err` then exits >0
    die()   { err "$@" && exit 11; }
# }}}

prepend_items() { #{{{
    # Usage: prepend_items 'delimiter' "list of args to prepend w/ delimiter"
    #        Include single-quoted <space> in delimiter if desired.
    Delim=${1} && shift || echo "ERROR in 'joined' delimiter missing." >2
    List=( $@ )
    [[ "$Delim" =~ '-' ]] && Delim=${Delim//-/\\-} && hyphens=True #escape hyphens for 'printf'
    prepended=$(printf "${Delim}%s " ${List[@]});
    [[ -n ${hyphens} ]] && prepended=${prepended//\\-/-}
    echo "$prepended"
} #}}}

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ Variables ~~~~~
App=${1:-"jaxid_generator"}
DjangoAdmin=${2:-"bleopold"}
FromEmail='db_backup@mbiomecore'

Today=$(get_datestamp_ymd)

Format="json"
DjangoAppPath="/var/www/apps/${App}"
BackupFile="${DjangoAppPath}/backups/${Today}.db.${App}.${Format}"

#Exclusions=$(prepend_items '-e ' sessions contenttypes auth admin.logentry)
Exclusions=$(prepend_items '-e ' sessions contenttypes)

EmailTo=${DjangoAdmin}@jax.org

#~~~~~~~~~~~~~~~~~~~~~~ Rsync Vars ~~~~~ #{{{
ArchiveHost='ctdtn02'
ArchivePath='/tier2/mbiomecore/data/jaxid/database'

SshOpts='-e "ssh -o StrictHostKeyChecking=no"'
RsyncOpts='--quiet --times --links --compress'
RsyncOpts+=' --no-group --chmod=Dg+sx,Fug=r,o-rwx'
RsyncCmd="rsync ${RsyncOpts} ${SshOpts} ${BackupFile}.gz ${ArchiveHost}:${ArchivePath}"
#debug "Rsync Backup Cmd: $RsyncCmd"
#}}}


#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ Back Me Up! Dump Me Out! ~~~~~

print "Beginning data dump of '$App' django database."

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
    && gzip -vf9N ${BackupFile}

    SuccessfulRsync=$(eval $RsyncCmd)
    RsyncCheck=$(ssh ${ArchiveHost} "stat -t ${ArchivePath}/$(basename ${BackupFile}).gz")
fi

if [[ -f "${BackupFile}.gz" ]]; then
    print "Database dump now at: ${BackupFile}.gz"
    Msg="Database dump attached:
    ${BackupFile}.gz\n"
    if [[ "$RsyncCheck" ]]; then
      Msg+="\nDB backup is succesfully rsync'd to server:
      ${ArchiveHost}:${ArchivePath}/${BackupFile}.gz"
    fi
    Subj="'$App' database backup completed on ${Today}"
    File="-a ${BackupFile}.gz"
else
    print "Database dump ERROR??: ${BackupFile}.gz"
    Msg="Database dump error?
    ${BackupFile}.gz
    Please find out why that file does not exist."
    Subj="'$App' database backup ERROR on ${Today}"
    File=""
fi

print "Emailing the backup results."

print "${Msg}" |     \
    mail ${File}    \
    -r ${FromEmail} \
    -s "${Subj}"    \
    ${EmailTo}

print "DB Backup Script completed"


# vim: ft=sh fdm=marker:
