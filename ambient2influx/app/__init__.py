from flask import Flask

app = Flask(__name__)

from app import routes

import logging

app.logger.setLevel(logging.DEBUG)
logging.getLogger('gunicorn.error').setLevel(logging.DEBUG)
logging.getLogger('gunicorn.access').setLevel(logging.DEBUG)
app.logger.info("Flask app started successfully")