lol
![A Dumb Example](/docs/wow.gif)

# Changed a bunch of shit

Now you need env variables instead of the config file :)

# Make sure these are configured on the host
1) DATABASE_URL
   1) postgres://user:pass@url:port/schema
2) FLASK_APP
   1) project
3) FLASK_SECRET_KEY
   1) A long random string for random sessions and stuff
4) FLASK_ENV
   1) development/production

# How 2 Run

1) Enable venv
  * `.\env\Scripts\activate`
2) Start flask
  * `flask run`
# If using something like AWS or Heroku
Setting up [Postgres on Heroku](https://devcenter.heroku.com/articles/heroku-postgresql).

![A bad example](/docs/config_vars_heroku.png)
