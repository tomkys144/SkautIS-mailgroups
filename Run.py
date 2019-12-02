import App
import yaml
from bottle import post, route, request, run, response

skautis_token = None


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
    if cfg['domain'] != '':
        response.body = 'Busy'
    else:
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
    skautis_token = request.post
    App.checker(skautis_token, App.cfg['unit'])


@route('/logout')
def logout():
    logout_link = App.skautis.get_logout_url(skautis_token)
    return logout_link


run(host=App.cfg['IP'], port=8080, debug=True)
