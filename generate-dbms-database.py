#!/usr/bin/env python3
"""
Setup student databases and permissions
"""

import subprocess
from glob import glob
from pathlib import Path

USER_FILE_PATH = '/home/*/dbms_users.txt'
DATABASE_FILE_PATH = '/opt/dbms-student-databases/databases/*.sql.gz'

DATABASES = [Path(db).name.split('.sql.gz')[0]
             for db in glob(DATABASE_FILE_PATH)]

cmd = []
for users in glob(USER_FILE_PATH):
    with open(users) as f:

        # create the test database
        cmd.append('createdb -E UTF8 -O postgres test')

        # create the exam databases
        for db in DATABASES:
            cmd.append(f'createdb -E UTF8 -O postgres {db}')
            cmd.append(f'zcat /root/databases/{db}.sql.gz |psql {db}')

        for user in f:
            if not user.strip() or user.startswith("#"):
                continue

            user_name = user.split("@")[0]
            user_pass = user.split(".")[0].capitalize() + "7000"

            cmd.append(f'\n# {user.strip()}')
            cmd.append('# ------------------------------')
            cmd.append(f"createuser {user_name}")
            cmd.append(f"echo \"ALTER USER \\\"{user_name}\\\" PASSWORD '{user_pass}'\" | psql postgres")
            for db in DATABASES + ['test']:
                # access to the default database
                cmd.append(f"echo \"GRANT CONNECT ON DATABASE {db} TO \\\"{user_name}\\\";\"|psql {db}")
                cmd.append(f"echo \"GRANT USAGE ON SCHEMA public TO \\\"{user_name}\\\";\"|psql {db}")

                db_name = f"{db}.{user_name}"
                cmd.append(f"echo \"DROP DATABASE IF EXISTS \\\"{db_name}\\\"; CREATE DATABASE \\\"{db_name}\\\" WITH TEMPLATE \\\"{db}\\\" OWNER \\\"{user_name}\\\"; GRANT ALL PRIVILEGES ON DATABASE \\\"{db_name}\\\" TO \\\"{user_name}\\\"\" | psql postgres")
                cmd.append(f"echo \"GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO \\\"{user_name}\\\"\" | psql {db_name}")

# execute the database commands
subprocess.run(['/bin/bash'], input='\n'.join(cmd).encode('utf-8'))
