lol
![A Dumb Example](/docs/test.gif)

# Changed a bunch of shit

Now you need env variables instead of the config file :)

# Make sure these are configured on the host
1) DATABASE_URL
   1) postgres://user:pass@url:port/schema
2) FLASK_ENV
   1) development/production

# If using something like AWS or Heroku
Setting up [Postgres on Heroku](https://devcenter.heroku.com/articles/heroku-postgresql).

![A bad example](/docs/config_vars_heroku.png)

