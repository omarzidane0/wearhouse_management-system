import random
import secrets

def token_generate():
    token = secrets.token_urlsafe(32)
    return token
