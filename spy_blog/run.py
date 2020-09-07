import os
from dotenv import load_dotenv

load_dotenv('.flaskenv', override=True, verbose=True)
load_dotenv('.env', override=True, verbose=True)

from app import create_app

app = create_app(os.getenv('FLASK_ENV', 'development'))


if __name__ == '__main__':
    app.run()