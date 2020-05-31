import os
from flask import Flask, render_template, request,send_from_directory

app = Flask(__name__)
app.debug=True

@app.route('/')
def home():
    return send_from_directory('static','index.html')

@app.route('/about')
def about():
    return send_from_directory('static','about.html')


@app.route('/static/<path:path>')
def send_js(path):
    return send_from_directory('static', path)

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)