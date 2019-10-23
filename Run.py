import App
from bottle import route, request, template, run, redirect


@route('/')
def land():
    return template('login', login_link=App.login_link)


@route('/login')
def login():
    skautis_token = request.forms.get('skautIS_Token')
    App.checker(skautis_token, App.cfg['unit'])
    logout_link = App.skautis.get_logout_url(skautis_token)
    redirect(logout_link)


run(host=App.cfg['IP'], port=8080, debug=True)
