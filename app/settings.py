import logging
import os


SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL', 'sqlite:///')
SECRET_KEY = os.environ.get('SECRET_KEY', '')

LOG_LEVEL = os.environ.get('LOG_LEVEL', logging.INFO)

BAN_IPS = [ip_mask for ip_mask in os.environ.get('BAN_IPS', '').split(',') if ip_mask]
