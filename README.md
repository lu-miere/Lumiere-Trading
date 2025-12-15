Environment Setup

# Start and build Services:

every service is prefixed with 'lumiere' in Dcker

(api, ui, db, redis)

# restarts all defined services

# runs the svc i the background

# forces Docker to rebuild the images (if any changes)

- docker compose up -d --build

# Check Status

docker compose ps
ose

# Command Execution

- Becuase we use poetry to manage dependencies and the virtual env, we must use poetry in the command to ensure the correct python interpreter and executes the libraries installed in the Poetry environemnt.
- cli service added in the compose.yml this has allowed us to shorten the entire command to make changes from within in the docker container itself from

docker compose run api poetry run python manage.py [command]
to
docker compose run cli [command]

# generate new migration file

docker compose run cli makemigrations

# apply all pending migrations

docker compose run --rm cli miograte
