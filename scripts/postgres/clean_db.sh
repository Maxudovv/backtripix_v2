# Drop connections to the existing database
docker exec tripix-pg psql -U tripix_user -c "UPDATE pg_database SET datallowconn = 'false' WHERE datname='tripix_db'" postgres
docker exec tripix-pg psql -U tripix_user -c "SELECT pg_terminate_backend(pid) FROM pg_stat_activity WHERE datname='tripix_db'" postgres

# Create empty database
docker exec tripix-pg psql -U tripix_user -c "DROP DATABASE tripix_db" postgres
docker exec tripix-pg psql -U tripix_user -c "CREATE DATABASE tripix_db" postgres

# Fill db
cd backend
pipenv run python manage.py migrate
#pipenv run python manage.py fill_db_for_dev
