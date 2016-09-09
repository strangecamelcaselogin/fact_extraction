from flask import Flask
from flask import render_template, redirect, flash, \
    request, session, abort, g, url_for

from core import Core


app = Flask(__name__)


@app.route('/')
def hello_world():
    temp_filename = 'test.txt'
    c = Core()
    c.run(temp_filename)
    return 'web test'

if __name__ == '__main__':
    app.run(debug=True)