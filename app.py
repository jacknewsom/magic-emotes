from flask import Flask, request, jsonify, send_file
from utils import magic_emote_supported, get_magic_emote_filename

app = Flask(__name__)

@app.route('/', methods=['GET'])
def index():
    if request.method == 'GET':
        tokens = [request.args.get(k, None) for k in request.args if request.args.get(k, None) != None]
        return f'Found tokens {tokens}'

@app.route('/api/emote', methods=['GET'])
def emote():
    if 'content' not in request.args or 'style' not in request.args:
        return {'error': 'invalid request. must contain "content" and "style" keys but both were not present'}
    content, style = request.args['content'], request.args['style']

    # check if this magic emote is supported yet
    if not magic_emote_supported(content, style):
        return {'error': f'magic emote {content}+{style} not supported'}

    return send_file(get_magic_emote_filename(content, style))