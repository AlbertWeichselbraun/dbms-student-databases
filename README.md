# dbms-student-databases
Scripts for setting up student databases.

Per default the scripts searches for the e-mail addresses of users in 
   /home/*/dbms_users.txt
and then setups a test database as well as the example databases for the specified users.


## Install

These instructions assume that you have postgres installed and running on your system, and that the bash shell is available.

Checkout this repository into your `/opt` directory. 

- `/opt/databases` ... a directory that contains the gziped SQL files of the databases to set up.
- `/opt/dbms-student-databases/generate-dbms-database.py` ... script used for setting up the student databases.


## Manually run the script

To let other users manually run the script create a `/etc/sudoers` entry such as

```sudo
# allow members of the dbms group to update the user lists
%dbms ALL=(postgres) /opt/dbms-student-databases/generate-dbms-database.py
```

Users can then run the script with
```bash
sudo -u postgres /opt/dbms-student-databases/generate-dbms-database.py
```

## Run via crontab

This resets the student's database on a daily basis.

```crontab
17 6    * * *   postgres /opt/dbms-student-databases/generate-dbms-database.py
```

