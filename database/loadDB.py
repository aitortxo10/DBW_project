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
sthLP = "INSERT INTO languages_challenges VALUES ({});"
sthCP = "INSERT INTO categories_challenges VALUES ({});"

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
                        l_id = c.fetchone() # returns tuple with (id, name) or None if empty
                        print(l_id)

                        # if language not yet in the table
                        if not l_id:
                            to_exec = "INSERT INTO programming_languages (name) VALUES ({});".format("'" + lang + "'")
                            print(to_exec)
                            c.execute(to_exec)
                            l_id = c.lastrowid
                        else:
                            l_id = l_id[0]
                        # add the languages available into the languages_challenges table
                        comm = sthLP.format("'" + str(c_id) + "'," +  "'" + str(l_id) + "'," + "'example_code'")
                        print(comm)
                        c.execute(comm)

            elif (column == "Categories"):
                # this will occur after loading the challenge in the table and filling the languages_challenges table
                for cat in value.strip().split(","):
                    print(cat)
                    with connection.cursor() as c:
                        com = "SELECT id FROM categories WHERE name = {};".format("'" + cat + "'")
                        c.execute(com)
                        cat_id = c.fetchone() # returns tuple with (id, name) or None if empty
                        # if the cat    egory was not already in the categories table, load it
                        if not cat_id:
                            to_exec = "INSERT INTO categories (name) VALUES ({});".format("'" + cat + "'")
                            c.execute(to_exec)
                            cat_id = c.lastrowid
                        else:
                            cat_id = cat_id[0] # get the id from the tuple

                        comm = sthCP.format("'" + str(cat_id) + "'," + "'" + str(c_id) + "'")
                        c.execute(comm)

            else:
                # construct a single string with all the column, values in the same order
                # to use in the SQL command
                columns += (column + ", ")
                values += ("'" + value + "', ")
