# Run JAXID database dump for backup once a week on Sunday at 1am by default
0 1 * * Sun bleopold /var/www/apps/jaxid_generator/dbs/dumpdata_django_db.sh 

