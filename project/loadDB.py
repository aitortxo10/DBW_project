import pymysql
import os

# Connect to database
database = "mydb"
host = "localhost"
user = "root"
passwd = "password"

connection = pymysql.connect(host='localhost',
                user=user,
                password=passwd,
                db=database,
                charset='utf8mb4',
                autocommit=True
            )

# Turn off FKs
connection.cursor().execute("SET FOREIGN_KEY_CHECKS=0")

# loading challenges from the folder problems/
sthProblems = "INSERT INTO challenges ({}) VALUES ({});"
for problem in os.listdir("problems"):
    with open("problems/"+problem, 'r') as fh:

        columns = ""
        values = ""

        # from each line extract the content and the column of the table where it belongs
        for line in fh:
            line = line.rstrip()
            column, value = line.split(" ; ")

            # ignore empty lines
            if not column or not value:
                continue

            # construct a single string with all the column, values in the same order
            # to use in the SQL command
            columns += (column + ", ")
            values += ("'" + value + "', ")

        command = sthProblems.format(columns[:-2], values[:-2])
        print(command)
        with connection.cursor() as c:
            c.execute(command)
        print(problem)

# manually loading the programming languages
sthLanguages = "INSERT INTO programming_languages ({}) VALUES ('{}');"
languages = ["Python 3.8", "Perl 5", "R 4.0.2"]
i = 0
for language in languages:
    command = sthLanguages.format("name, id", language + "', '" + str(i))
    print(command)
    with connection.cursor() as c:
        c.execute(command)
    print(language)
    i += 1
