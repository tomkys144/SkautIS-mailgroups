import App
import yaml
from bottle import post, route, request, run, response

skautis_token = None


@post('/setup')
def setup():
    with open('./conf/config.yml') as config:
        cfg = yaml.safe_load(config)
    response.content_type = 'application/json'
    data = request.json
    login_link = App.login_link
    cfg['domain'] = data['domain']
    cfg['unit'] = data['unit']
    with open('./conf/config.yml', 'w') as file:
        yaml.safe_dump(cfg, file)
    return login_link


@route('/start')
def start():
    global skautis_token
    skautis_token = ''
    App.checker(skautis_token, App.cfg['unit'])


@route('/logout')
def logout():
    logout_link = App.skautis.get_logout_url(skautis_token)


run(host=App.cfg['IP'], port=8080, debug=True)
