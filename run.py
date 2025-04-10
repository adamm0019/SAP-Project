from app import create_app, db
from app.models import User, Message
from config import DevelopmentConfig

app = create_app(DevelopmentConfig)

@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'User': User, 'Message': Message}

if __name__ == '__main__':
    app.run(debug=True, host='127.0.0.1', port=5000)