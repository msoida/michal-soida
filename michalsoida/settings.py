from decouple import config, Csv

host = config('HOST', default='0.0.0.0')
port = config('PORT', default=5000, cast=int)
debug = config('DEBUG', default=False, cast=bool)
secret_key = config('SECRET_KEY')
postgres_db = config('POSTGRES_DB')
postgres_user = config('POSTGRES_USER')
