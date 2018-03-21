#!/usr/bin/python3
import sys
import sqlite3

conn = sqlite3.connect('classes.db');
cursor = conn.cursor();

# Init sql database
cursor.execute("CREATE TABLE IF NOT EXISTS classes (className text, PRIMARY KEY(className))")
cursor.execute("CREATE TABLE IF NOT EXISTS assignments (className text, name text, weight real, grade real)")

def create_class(className):
    print("creating class {}".format(className))
    cursor.execute('INSERT INTO classes (className) VALUES (?)', [className])
    conn.commit()

def create_assignment(className, name, weight, grade):
    print("creating assignment {}:{}\n".format(name, className))
    cursor.execute('INSERT INTO assignments VALUES (?, ?, ?, ?)', (className, name, weight, grade))
    conn.commit()

def get_all_classes():
    print("Current Grades:\n")
    print("Class\t\t Grade")
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

def get_all_classes_extended():
    cursor.execute("SELECT className FROM classes")
    temp = cursor.fetchall()
    for row in temp:
        get_class_extended(row[0])
        print("\n")

def get_class(className):
    cursor.execute("SELECT className, SUM(grade * (weight / 100)) as grade FROM assignments WHERE className = ? GROUP BY className", [className])
    res = cursor.fetchone()
    print("Class: {}, Grade: {}".format(res[0], round(res[1], 2)))

def get_class_extended(className):
    print("Current Grade for {}\n".format(className))
    print("Assignment\t\t Weight\t\t Grade\t\t Normalized")
    print("-------------------------------------------------------------------\n")
    total = 0
    for row in cursor.execute('SELECT name, weight, grade, grade * (weight / 100) FROM assignments WHERE className = ?', [className]):
        print("{}\t\t\t {}\t\t {}\t\t {}\t\t".format(row[0], row[1], row[2], round(row[3], 2)))
        total += round(row[3], 2)
    print("\nTotal Average:\t\t\t\t\t\t {}".format(total))

if (len(sys.argv) >= 4 and sys.argv[1] == "create"):
    if (len(sys.argv) == 7 and sys.argv[2] == "assignment"):
        create_assignment(sys.argv[3], sys.argv[4], sys.argv[5], sys.argv[6])
    elif (sys.argv[2] == "class"):
        create_class(sys.argv[3])
    else:
        print ("Unable to parese 'create' command!\n")

if (len(sys.argv) >= 2 and sys.argv[1] == "print"):
    if (len(sys.argv) >= 3 and sys.argv[2] == "extended"):
        if (len(sys.argv) >= 4):
            for i in range(3, len(sys.argv)):
                get_class_extended(sys.argv[i])
                print("\n")
        else:
            get_all_classes_extended()
    elif (len(sys.argv) >= 3):
        for i in range(2, len(sys.argv)):
            get_class(sys.argv[i])
    else:
        get_all_classes()

cursor.close()
conn.close()
