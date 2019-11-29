import App
import yaml
from bottle import post, route, request, run, response

skautis_token = None


@post('/setup')
def setup():
    with open('./conf/config.yml') as config:
        cfg = yaml.safe_load(config)
    data = request.json
    login_link = App.login_link
    if cfg['domain'] != '':
        response.status = 503
    else:
        cfg['domain'] = data['domain']
        cfg['unit'] = data['unit']
        with open('./conf/config.yml', 'w') as file:
            yaml.safe_dump(cfg, file)
        response.body = login_link
    return response


@route('/start')
def start():
    global skautis_token
    skautis_token = request.post
    App.checker(skautis_token, App.cfg['unit'])


@route('/logout')
def logout():
    logout_link = App.skautis.get_logout_url(skautis_token)
    return logout_link


run(host=App.cfg['IP'], port=8080, debug=True)
