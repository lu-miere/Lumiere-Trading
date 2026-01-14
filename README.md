# Lumiere Trading

Trading application that allows users:
1. to log trades and provide metrics based on given account trading history
2. journal trades and view entries as a timweline
3. search and save core fundamental data such as headline and economic releases
4. stream prices
5. perform technical analysis and log the analysis to the journal
6. backtest algorithmic strategies (proprietary or use existing API?)

## Tech Stack (updating...)

Framework: Django 4.2+
Database: PostgreSQL
Dependency Management: Poetry
Infrastructure: Docker, Nginx, Gunicorn

## Dependency Management

The project uses poetry instead of a requirements.txt for tighter dependancy management.

Local Setup:
-make sure poetry is installed
-Install dependencies: poetry install

To add new dependencies:
poetry add ["dependency"]

## Docker

-every service is prefixed with 'lumiere'
(api, ui, db, redis)

1. clone the repository
2. build and launch:
   docker compose up --build

to run a command:
docker compose run cli

# Overview of repo structure
