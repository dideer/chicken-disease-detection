import os

# PostgreSQL database credentials & connection
DB_NAME = os.getenv('DB_NAME', 'chicken_db')
DB_USER = os.getenv('DB_USER', 'chicken_user')
DB_PASSWORD = os.getenv('DB_PASSWORD', 'Ishimwe123')
DB_HOST = os.getenv('DB_HOST', 'localhost')
DB_PORT = os.getenv('DB_PORT', '5432')

# Application security
SECRET_KEY = os.getenv('SECRET_KEY', 'poultry-disease-admin-secret')
TOKEN_MAX_AGE_SECONDS = int(os.getenv('TOKEN_MAX_AGE_SECONDS', '86400'))

# Default admin bootstrap
DEFAULT_ADMIN_USERNAME = os.getenv('DEFAULT_ADMIN_USERNAME', 'admin')
DEFAULT_ADMIN_EMAIL = os.getenv('DEFAULT_ADMIN_EMAIL', 'admin@poultry.local')
DEFAULT_ADMIN_PASSWORD = os.getenv('DEFAULT_ADMIN_PASSWORD', 'admin123')
