class Config(object):
    DEBUG = False
    DATABASE_HOST = ""
    DATABASE_PORT = 5432
    DATABASE_USER = "postgres"
    DATABASE_PASS = "postgres"
    DATABASE_SCHEMA = "raffle_entries"

class Development(Config):
    DEBUG = True 

class Production(Config):
    pass

app_config = {
    'dev': Development,
    'prd': Production
}