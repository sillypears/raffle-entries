# Environment Variables
How to set environment variables
Either set these on your platform or turn them into a script

## Linux
export DATABASE_URL=postgres://<user>:<pass>@<host>:<port>/<schema>
export FLASK_ENV=<environment>
export FLASK_SECRET_KEY=<random key>

## Batch
set DATABASE_URL=postgres://<user>:<pass>@<host>:<port>/<schema>
set FLASK_ENV=<environment>
set FLASK_SECRET_KEY=<random key>

## Powershell
$env:DATABASE_URL='postgres://<user>:<pass>@<host>:<port>/<schema>'
$env:export FLASK_ENV='<environment>'
$env:FLASK_SECRET_KEY='<random key>'