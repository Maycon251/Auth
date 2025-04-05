from flask import Flask, render_template, send_from_directory, request, jsonify, abort, redirect
from logging import getLogger, ERROR
from dotenv import load_dotenv

log = getLogger('werkzeug')
log.setLevel(ERROR)
load_dotenv()


app = Flask(__name__, static_folder='../front/dist/browser')

@app.route('/<path:filename>')
def serve_static_files(filename):
    return send_from_directory(app.static_folder, filename)

