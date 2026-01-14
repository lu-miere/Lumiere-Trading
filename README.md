# Environment Setup

1. Start and build Services:

every service is prefixed with 'lumiere' in Docker

(api, ui, db, redis)

# restarts all defined services

# runs the svc i the background

# forces Docker to rebuild the images (if any changes)

- docker compose up -d --build

# check contianer status

The check command: This is a built-in Django tool that inspects your project for:

Syntax Errors: Typos in your Python files.
System Check Framework: It checks if your models are valid (e.g., "Field 'X' doesn't exist").
Compatibility: Ensures your settings (like INSTALLED_APPS) are configured correctly.

Circular Imports: It identifies if File A is trying to import File B, while File B is trying to import File A (a common cause of the "Worker failed to boot" error you saw earlier).
docker compose run -rm _container_ pytohn manage,py check

# Check Status

docker compose ps

2. Commands

# one off tasks

docker compose run

- Becuase we use poetry to manage dependencies and the virtual env, we must use poetry in the command to ensure the correct python interpreter and executes the libraries installed in the Poetry environemnt.
- cli service added in the compose.yml this has allowed us to shorten the entire command to make changes from within in the docker container itself from

docker compose run api poetry run python manage.py [command]
to
docker compose run cli [command]

# generate new migration file

docker compose run cli makemigrations

# apply all pending migrations

docker compose run --rm cli miograte

# Overview of repo structure
