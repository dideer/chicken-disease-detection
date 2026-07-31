# app/utils/helpers.py
# Utilities: password hashing/checking, multi-language messages

from flask_bcrypt import Bcrypt

MESSAGES = {
    'register_success': {
        'en': 'User registered successfully',
        'rw': 'Umukoresha yanditswe neza',
        'fr': 'Utilisateur enregistré avec succès'
    },
    'register_exists': {
        'en': 'Username or email already exists',
        'rw': 'Izina ry’umukoresha cyangwa email biriho',
        'fr': 'Nom d’utilisateur ou email déjà utilisé'
    },
    'register_error': {
        'en': 'Registration failed',
        'rw': 'Kwiyandikisha byanze',
        'fr': "Échec de l'inscription"
    },
    'login_success': {
        'en': 'Login successful',
        'rw': 'Kwinjira byagenze neza',
        'fr': 'Connexion réussie'
    },
    'login_invalid': {
        'en': 'Invalid username or password',
        'rw': 'Izina ry’umukoresha cyangwa ijambo banga si byo',
        'fr': 'Nom d’utilisateur ou mot de passe invalide'
    },
    'login_error': {
        'en': 'Login failed',
        'rw': 'Kwinjira byanze',
        'fr': 'Échec de la connexion'
    }
}

def get_message(key, lang='en'):
    return MESSAGES.get(key, {}).get(lang, MESSAGES.get(key, {}).get('en', ''))

def hash_password(bcrypt, password):
    return bcrypt.generate_password_hash(password).decode('utf-8')

def check_password(bcrypt, hashed, password):
    return bcrypt.check_password_hash(hashed, password)
