import os

class Config(object):
    SECRET_KEY = os.environ.get("SECRET_KEY") or "secret_string"
    MONGODB_SETTINGS = {'host':os.environ.get("DB_URL")}

    APP_ROOT = os.path.dirname(os.path.abspath(__file__))
    print(APP_ROOT)
    for file in os.listdir(APP_ROOT):
        print(str(file))
    
    UPLOAD_FOLDER = os.path.join(APP_ROOT, 'app/static/runtime_files/')
    DOWNLOADS_FOLDER = os.path.join(APP_ROOT, 'app/static/downloads/')
