pg_dump -U username -f backup.sql database_name
psql -d database_name -f backup.sql