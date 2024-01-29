import json

from flask import Flask
from routes import routes

app = Flask(__name__)

app.add_url_rule('/', 'index', routes.index)
app.add_url_rule('/chat', 'chat', routes.chat, methods=['POST'])
app.add_url_rule('/clear_messages', 'clear_messages', routes.clear_messages, methods=['POST'])

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, debug=True)