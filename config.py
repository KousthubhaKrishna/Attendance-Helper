import os

class Config(object):
    SECRET_KEY = os.environ.get("SECRET_KEY") or "secret_string"
    MONGODB_SETTINGS = {'host':os.environ.get("DB_URL")}
    UPLOAD_FOLDER = './app/static/runtime_files/'
    DOWNLOADS_FOLDER = './app/static/downloads/'
