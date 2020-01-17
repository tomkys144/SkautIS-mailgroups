import App
import yaml
from bottle import post, route, request, run, response, redirect
import os

skautis_token = None
redir_link = None


@route('/check')
def check():
    data = request.post
    if data == 'check login':
        if skautis_token is not None:
            response.body = 'logged in'
            return response
        else:
            response.body = 'not logged in'
            return response
    else:
        response.status = 400
        return response

@post('/setup')
def setup():
    with open('./conf/config.yml') as config:
        cfg = yaml.safe_load(config)
    data = request.json
    if cfg['domain'] != '' or cfg['unit'] != '':
        response.body = 'Busy'
    else:
        global redir_link
        redir_link = data['page']
        login_link = App.loginer(redir_link)
        cfg['domain'] = data['domain']
        cfg['unit'] = data['unit']
        with open('./conf/config.yml', 'w') as file:
            yaml.safe_dump(cfg, file)
        response.body = login_link
    return response


@route('/start')
def start():
    global skautis_token
    skautis_token = request.post['skautIS_Token']
    App.checker(skautis_token, App.cfg['unit'])
    logout_link = App.skautis.get_logout_url(skautis_token)
    response.body = logout_link
    skautis_token = None
    return response


@route('/checker')
def checker():
    return('works')


port = os.environ.get('PORT', 5000)

run(host=App.cfg['IP'], port=port, debug=True)
