#!/usr/bin/env bash

#-------------------------------------------------------------------------------
#       Check if jaxID db has been modified, then back it up to repo           -
#-------------------------------------------------------------------------------

## check if db has been changed
DBPATH=/var/www/django/jaxid_generator
DBNAME=db.sqlite3


#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ Run it! ~~~~~
cd $DBPATH
MOD=$(git status --porcelain --untracked=no | grep $DBNAME | cut -c2,2)

if [[ "$MOD" == "M" ]]; then
    ## git add, git commit; git push origin master
    git add -v $DBNAME
    git add -v id_generate/migrations/
    git commit -m "latest db update backup"
    git push --porcelain origin master
fi

