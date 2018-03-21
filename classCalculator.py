#!/usr/bin/python3
import sys
import sqlite3

conn = sqlite3.connect('classes.db');
cursor = conn.cursor();

# Init sql database
cursor.execute("CREATE TABLE IF NOT EXISTS classes (className text)")
cursor.execute("CREATE TABLE IF NOT EXISTS assignments (className text, name text, weight real, grade real)")

def create_class(className):
    print("creating class {}".format(className))
    cursor.execute('INSERT INTO classes VALUES (?)', [className])
    conn.commit()

def create_assignment(className, name, weight, grade):
    print("creating assignment {}:{}\n".format(name, className))
    cursor.execute('INSERT INTO assignments VALUES (?, ?, ?, ?)', (className, name, weight, grade))
    conn.commit()

def get_all_assignments():
    print("Current Grades:\n")
    print("Class\t\t Grade\n")
    print("----------------------\n")

    for row in cursor.execute(
        '''SELECT
            c.className as class,
            a.grade as grade
        FROM
            classes as c
            JOIN (SELECT className, SUM(grade * (weight / 100)) as grade FROM assignments GROUP BY className) as a
            ON a.className == c.className'''):
        print("{}\t\t {}".format(row[0], round(row[1], 2)))



if (len(sys.argv) >= 4 and sys.argv[1] == "create"):
    if (len(sys.argv) == 7 and sys.argv[2] == "assignment"):
        create_assignment(sys.argv[3], sys.argv[4], sys.argv[5], sys.argv[6])
    elif (sys.argv[2] == "class"):
        create_class(sys.argv[3])
    else:
        print ("Unable to parese 'create' command!\n")

if (len(sys.argv) >= 2 and sys.argv[1] == "print"):
    get_all_assignments()
