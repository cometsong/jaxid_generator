#!/usr/bin/env python3
"""
File: jaxid_generator.py
Author: Benjamin Leopold (cometsong)
Created: 2015-01-13 09:15:00-0500
Description: Create and check uniqueness of a new JAXid
Requirements: python3, pymysql, MySQL
"""

"""
TODO: add interactive approach for end user to validate then insert
TODO: add batch mode to create multiple jaxids (via optparse) and then send same list to put_jaxid
TODO: create django interface for end users
"""

import sys
import string
import random
import argparse

import pymysql

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ Specs ~~~~~
__author__ = 'Benjamin Leopold'
__copyright__ = 'Copyright 2014 Benjamin Leopold'
__version__ = '0.2'
__status__ = 'Development'
__program__ = 'JAXid_generator'

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ Classiness ~~~~~
class RandomID(object):
    """RandomID generates a string of random alphanumeric chars"""
    def __init__(self):
        self.size = 10

    def generate(self, size=0, chars=string.ascii_uppercase + string.digits):
        """Generate random string of 'size' chars"""
        if size < 1:
            size = self.size
        return ''.join(random.choice(chars) for _ in range(size))


class JAXid_gen(RandomID):
    """Generate Random 5-char JAXID String"""
    def generate_id(self):
        """Use id_generator and add preceding 'J' character for the JAXid"""
        return ''.join(['J', super(JAXid_gen, self).generate(size=5)])


class JAXid_db(object):
    """db interaction with mysql db: jaxid_db"""
    def __init__(self, max_recurs=100, db_cfg_file=None):
        self.max = max_recurs
        self.db_cfg = self.load_db_cfg(db_cfg_file)
        self.idcon = self.db_connect()
        # do we still need to run "idcon.close()" or is it implicit at end?

        self.check_sql = "SELECT jaxid FROM jaxid_master WHERE jaxid=%s"
        self.insert_sql = "INSERT into jaxid_master SET jaxid=%s"

    def load_db_cfg(self, db_cfg_file):
        """load dict from external file"""
        try:
            dbfh = open(db_cfg_file, 'rt')
            exec(dbfh.read())
        except Exception as e:
            exit('DB_cfg Error! %s' % e)

    def db_connect(self):
        db = self.db_cfg
        return pymysql.connect(
            host=db['host'],
            port=db['port'],
            database=db['db'],
            user=db['user'],
            password=db['pswd']
            )

    def check_jaxid(self, jaxid):
        """query table in master id table in db for match"""
        found = False
        sql = self.check_sql
        idcur = self.idcon.cursor()
        idcur.execute(sql, jaxid)
        if idcur.rowcount > 0:
            found = True
        idcur.close()
        return found

    def put_jaxid(self, jaxid):
        """ insert accepted JAXid into db master table """
        sql = self.insert_sql
        idcur = self.idcon.cursor()
        idcur.execute(sql, (jaxid))
        self.idcon.commit()
        # check success?/error?
        found = self.check_jaxid(jaxid)
        idcur.close()
        if found:
            return ' '.join(["Successfully Inserted:", jaxid])
        else:
            return ' '.join(["Insert Error:", jaxid])

    def get_jaxid(self, count=1):
        """
        generate new JAXid
        check existence in master table
        call recursive if so
        NOTE: Will take veeery long when we get a larger number of id values!!!
        """
        # count == max recursive end condition
        if count == self.max:
            return 'ERROR: Recursion Overload!'

        jaxid = JAXid_gen().generate()
        found = self.check_jaxid(jaxid)

        if found:
            return self.get_jaxid(count=count+1)
        else:
            return jaxid



#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ Functional ~~~~~
def parse_args(argv):
    parser = argparse.ArgumentParser(
        prog=__program__,
        description='generate, get, insert JAXids, plate ids, etc')
    parser.add_argument(
        '-c', '--count', dest='count', default=1, type=int,
        help='the number of IDs to generate')
    parser.add_argument(
        '-t', '--type', dest='idtype', default='j', type=str,
        choices=['j', 'p', 'b', 'jaxid', 'plateid', 'boxid'],
        help='the type of IDs to generate')
    parser.add_argument(
        '--log', default=sys.stdout, type=argparse.FileType('w'),
        help='the file where the log should be written')
    parser.add_argument(
        '--db_cfg', default='jaxid_db_cfg.py', type=argparse.FileType('r'),
        #help='file with database name and access info')
        help=argparse.SUPPRESS)
    return parser.parse_args(argv)


#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ Immediacy ~~~~~
if __name__ == '__main__':
    args = parse_args(sys.argv)
    DEBUG = True
    jdb = JAXid_db(db_cfg_file=args.db_cfg)
    jaxid = jdb.get_jaxid(args.count)
    if DEBUG: print(' '.join(["JAXID:", jaxid]))
    #ok = (ask if JAXID is ok to use)
    #if ok: jdb.put_jaxid(jaxid)
    #print(jdb.put_jaxid(jaxid))
