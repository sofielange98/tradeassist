to run locally, first clone the repository
requires python 3
run the following once the repo is on your machine
cd tradeassist
# activate the virtual environment
source app/app_env/bin/activate
# configure for dev
export FLASK_ENV=development
# create the database
flask init-db
# start the app
flask run
