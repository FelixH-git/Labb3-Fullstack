#!/usr/bin/env python3
#
# Demo mysql for dsd400-course
#
#
# python3 -m pip install PyMySQL
# debian package: python3-pymysql
#
# https://pymysql.readthedocs.io/en/latest/

import pymysql.cursors
import pprint

# Connect to the database
connection = pymysql.connect(host='dsd400.port0.org',
                             user="pyFHLK",
                             password='passwordlurigt'.encode().decode('latin1'),
                             database='labbgrupp1000',
                             charset='utf8mb4',
                             cursorclass=pymysql.cursors.DictCursor)

with connection:
    with connection.cursor() as cursor:
        # Read records
        cursor.execute("SELECT * FROM student")

        rum_result = cursor.fetchall()
        print(rum_result[-1].keys())

        # cursor.execute("SELECT * FROM student")
        # result = cursor.fetchall()
        # pprint.pp(result)
        
    with connection.cursor() as cursor:
        # Create a new record
        sql = "INSERT INTO student(IDstudent, Mejl_student, FullName) VALUES (%s, %s, %s)"
        cursor.execute(sql, (8, 'g@g.com', 'G'))

    # Note: autocommit is ON by default for MariaDB
    #
    # If autocommit is off we must commit to save changes.
    # connection.commit()
    #    
    # A TRANSACTION BEGIN forces autocommit off:
    # connection.begin()
    #
    # Then, commit or rollback:
    # connection.rollback()
    
    print()
    print('After insert:')
    with connection.cursor() as cursor:
        # Read records
        cursor.execute("SELECT * FROM student")
        result = cursor.fetchall()
        #pprint.pp(result)

    print()
    with connection.cursor() as cursor:
        # Read records
        sql = "DELETE FROM `student` WHERE (`FullName` = 'F')"
        cursor.execute(sql)
        #print("Rows deleted:", cursor.rowcount)