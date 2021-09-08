#
# WARNING: this script will reset your database cluster (i.e., delete all existing databases).
#
pg_dropcluster 12 main --stop; pg_createcluster 12 main; service postgresql start
