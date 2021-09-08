#!/usr/bin/env python3

DATABASES = ('projektdatenbank', 'unidb', 'world', 'bundesliga', 'wetterdaten')

for users in glob('/home/*/dbms_users.txt'):
    with open("users.txt") as f:
        print("createdb -E UTF8 -O postgres test")
        for db in DATABASES:
            print("createdb -E UTF8 -O postgres {}".format(db))
            print("zcat /root/databases/{}.sql.gz |psql {}".format(db, db))
    
        for user in f:
            if not user.strip() or user.startswith("#"):
                continue
    
            user_name = user.split("@")[0]
            user_pass = user.split(".")[0].capitalize() + "7000"
            
            print("\n# " + user.strip())
            print("# ------------------------------")
            print("createuser {}".format(user_name))
            print("echo \"ALTER USER \\\"{}\\\" PASSWORD '{}'\" | psql postgres".format(user_name, user_pass))
            for db in DATABASES + ('test', ): 
                # access to the default database
                print("echo \"GRANT CONNECT ON DATABASE {} TO \\\"{}\\\";\"|psql {}".format(db, user_name, db))
                print("echo \"GRANT USAGE ON SCHEMA public TO \\\"{}\\\";\"|psql {}".format(user_name, db))
    
                db_name = "{}.{}".format(db, user_name)
                print("echo \"DROP DATABASE IF EXISTS \\\"{}\\\"; CREATE DATABASE \\\"{}\\\" WITH TEMPLATE {} OWNER \\\"{}\\\"; GRANT ALL PRIVILEGES ON DATABASE \\\"{}\\\" TO \\\"{}\\\"\" | psql postgres".format(db_name, db_name, db, user_name, db_name, user_name))
                print("echo \"GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO \\\"{}\\\"\" | psql {}".format(user_name, db_name))
