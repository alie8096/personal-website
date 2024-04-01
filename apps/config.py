from sample import SUPER_USER


# Database configuration
DATABASE_USERNAME = SUPER_USER.username
DATABASE_PASSWORD = SUPER_USER.password
DATABASE_HOST = "localhost"  # Change if your database is on a different host
DATABASE_NAME = "site.db"
CSRF_ENABLED = True

# Secret key (replace with a long, random string)
# SECRET_KEY = 'T{;k#b.%4)V)8|S%E0?7J57z/N+(54~Wc]-zynbFQO43`85-={hV,1ML}_I9;I4'
SECRET_KEY = 'qwertyuiop{}asdfghjkl:zxcvbnm<>?~!@#$%^&*()_+=-0987654321`][POIUYTREWQASDFGHJKL;"\\ZXCVBNM,./]'

# Debug mode (set to False for production)
DEBUG = True
