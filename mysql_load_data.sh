usage="Usage: $(basename $0) <dbname> <datafilename>
    with first line of tab-separated datafile as column headers,
    and 4th section of file name as table: e.g. db.jaxid.devel.tablename.datetime.tsv"
database=${1:-jaxid_db_devel}
datafile=${2:-db.jaxid.orig.jaxiddetail.20171127.tsv}
user='root'
delimiter='\t'
fieldnames=$(head -n 1 ${datafile} | tr ${delimiter} ',')
echo "fieldnames: ${fieldnames}"
tablename="id_generate_$(echo ${datafile} | cut -d. -f4)"

echo "Loading data from file: ${datafile} into database: ${database} table: ${tablename}"
read -p "press return to continue...
"
mysql -v -u${user} -D${database} <<<"load data local infile '${datafile}' replace into table ${tablename} fields terminated by '${delimiter}' lines terminated by '\n' ignore 1 lines (${fieldnames});"
