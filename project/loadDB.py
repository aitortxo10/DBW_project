import pymysql
import os

# Connect to database
database = "mydb"
host = "localhost"
user = "arnau"
passwd = "Contrasenya"

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
sthLP = "INSERT INTO languages_challenges VALUES ({});"

for problem in os.listdir("problems"):
    with open("problems/"+problem, 'r') as fh:

        columns = ""
        values = ""

        # from each line extract the content and the column of the table where it belongs
        for line in fh:

            line = line.rstrip()
            if not line: # ignore empty lines
                continue

            column, value = line.split(" ; ")

            if (column == "Languages"): # this will be done when reaching the last lines of the file if it is in the correct format

                # As we have explored all the file already, include that information into the Challenges table
                command = sthProblems.format(columns[:-2], values[:-2]) # slicing to avoid last ","
                print(command)
                with connection.cursor() as c:
                    c.execute(command)
                    c_id = c.lastrowid # get challenge id

                # get all the languages that the problem can be solved in
                for lang in value.strip().split(","):
                    print(lang)
                    # check if language is in programming_languages table or not
                    with connection.cursor() as c:
                        com = "SELECT id FROM programming_languages WHERE name = {};".format("'" + lang + "'")
                        print(com)
                        c.execute(com)
                        l_id = c.fetchone()[0]
                        print(l_id)

                        # if language not yet in the table
                        if not l_id:
                            to_exec = "INSERT INTO programming_languages (name) VALUES ({});".format("'" + lang + "'")
                            print(to_exec)
                            c.execute(to_exec)
                            l_id = c.lastrowid


                        # add the languages available into the languages_challenges table
                        comm = sthLP.format("'" + str(c_id) + "'," +  "'" + str(l_id) + "'," + "'example_code'")
                        print(comm)
                        c.execute(comm)

            elif (column == "Categories"):
                # this will occur after loading the challenge in the table and filling the languages_challenges table
                pass

            else:
                # construct a single string with all the column, values in the same order
                # to use in the SQL command
                columns += (column + ", ")
                values += ("'" + value + "', ")
