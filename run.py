import os

from app import create_app

conf = os.getenv('FLASK_CONF', 'development')
app = create_app(conf)

if __name__ == '__main__':
    app.run()
