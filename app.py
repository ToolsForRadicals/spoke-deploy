from flask import Flask, flash, session, render_template, request, redirect, url_for
from flask_session import Session
import requests
from random import randrange
from auth0.v3.management import Auth0
from twilio.rest import Client
import os

country = os.getenv(('COUNTRY_CODE'),"AU")

app = Flask(__name__)
SESSION_TYPE = 'filesystem'
app.config.from_object(__name__)
Session(app)


app.debug = True
app.secret_key = "q9283jrisadjfklasdfoqiwe82934u329sdf"

def create_authzero_application(authzero_domain,authzero_token):
    mgmt_api_token = authzero_token
    auth0 = Auth0(authzero_domain, mgmt_api_token)
    params = dict()
    params['name'] = 'spoke{}'.format(str(randrange(1,99)))
    params['description'] = 'Spoke Authentication'
    params['app_type'] = 'spa'

    params['callbacks'] = list()
    params['callbacks'].append('https://{}.herokuapp.com/login-callback'.format(session['app_name']))
    params['callbacks'].append('http://{}.herokuapp.com/login-callback'.format(session['app_name']))

    params['allowed_logout_urls'] = list()
    params['allowed_logout_urls'].append('https://{}.herokuapp.com/logout-callback'.format(session['app_name']))
    params['allowed_logout_urls'].append('http://{}.herokuapp.com/logout-callback'.format(session['app_name']))

    params['web_origins'] = list()
    params['web_origins'].append('https://{}.herokuapp.com'.format(session['app_name']))
    params['web_origins'].append('http://{}.herokuapp.com'.format(session['app_name']))

    params['allowed_origins'] = list()
    params['allowed_origins'].append('https://*.{}.herokuapp.com'.format(session['app_name']))
    params['allowed_origins'].append('http://*.{}.herokuapp.com'.format(session['app_name']))

    params['oidc_conformant'] = False

    spoke_app_client = auth0.clients.create(params)

    rule_params = dict()

    rule_params['name'] = 'spokeuser{}'.format(str(randrange(1,99)))
    rule_params['script'] ='function (user, context, callback) {context.idToken["https://spoke/user_metadata"] = user.user_metadata; callback(null, user, context);}'
    rule_params['enabled'] = True

    rule_success = auth0.rules.create(rule_params)
    return spoke_app_client

def create_twilio_application(twilio_account_sid,twilio_auth_token):
    account_sid = twilio_account_sid
    auth_token = twilio_auth_token
    client = Client(account_sid, auth_token)

    friendly_name = 'spoke{}'.format(str(randrange(1,99)))
    inbound_request_url = 'https://{}.herokuapp.com/twilio'.format(session['app_name'])
    status_callback = 'https://{}.herokuapp.com/twilio-message-report'.format(session['app_name'])
    fallback_url = status_callback

    service = client.messaging \
                    .services \
                    .create(friendly_name=friendly_name,
                            inbound_request_url=inbound_request_url,
                            status_callback=status_callback,
                            fallback_url=fallback_url,
                        )
    numbers = client.available_phone_numbers(country) \
               .mobile \
               .list()

    number = client.incoming_phone_numbers \
              .create(phone_number=numbers[0].phone_number)

    phone_number = client.messaging \
                    .services(sid=service.sid) \
                    .phone_numbers \
                    .create(phone_number_sid=number.sid)
    return service

@app.route('/', methods=['GET', 'POST'])
def index():
    session['steps'] = 99
    return render_template("index.html")

@app.route('/steps')
def steps():
    return render_template("steps.html")

@app.route('/create_applications', methods=['GET','POST'])
def create_applications():
    session['authzero_domain'] = '{}.auth0.com'.format(request.form['authzero_domain'])
    session['authzero_token'] = request.form['authzero_token']
    session['twilio_account_sid'] = request.form['twilio_account_sid']
    session['twilio_auth_token'] = request.form['twilio_auth_token']
    try:
        authzero_result = create_authzero_application(session['authzero_domain'],session['authzero_token'])
        session['authzero_client_id'] = authzero_result['client_id']
        session['authzero_client_secret'] = authzero_result['client_secret']
    except Exception as e:
        error_message = "Couldn't create your Auth0 service. Double check your token and domain?.  The Error message was: {}".format(str(e))
        flash(error_message,"danger")
        return redirect(url_for("steps"))

    try:
        twilio_result = create_twilio_application(session['twilio_account_sid'],session['twilio_auth_token'])
        session['twilio_message_service_sid'] = twilio_result.sid
        
    except Exception as e:
        error_message = "Couldn't create your Twilio service. Double check your account sid and auth key?  The Error message was: {}".format(str(e))
        flash(error_message,"danger")
        return redirect(url_for("steps"))

    return redirect(url_for('create_heroku_deploy_button'))

@app.route('/check_heroku_name', methods=['POST'])
def check_heroku_name():
    session['app_name'] = request.form['app_name']
    desired_url = "https://api.heroku.com/apps/{}".format(session[
                                                          'app_name'])
    headers = {'Content-type': 'application/json',
               'Accept': 'application/vnd.heroku+json; version=3'}
    try:
        session['name_available'] = (requests.get(desired_url, headers=headers).json()['id'] == 'not_found')
        if session['name_available']:
            flash('Your Heroku Name is available!','success')
            return redirect(url_for('steps'))
    except:
        app_name_already_taken_message = 'Sorry, the name {} is already taken'.format(request.form['app_name'])
        flash(app_name_already_taken_message,"danger")
        return redirect(url_for('index'))



@app.route('/deploy')
def create_heroku_deploy_button():
    session['template'] = 'https://github.com/MoveOnOrg/Spoke/tree/v1.3'
    session['heroku_base_url'] = 'https://{}.herokuapp.com'.format(session['app_name'])
    deploy_url = '''
    https://heroku.com/deploy?
    template={template}&
    env[AUTH0_DOMAIN]={authzero_domain}&
    env[AUTH0_CLIENT_ID]={authzero_client_id}&
    env[AUTH0_CLIENT_SECRET]={authzero_client_secret}&
    env[BASE_URL]={heroku_base_url}&
    env[TWILIO_API_KEY]={twilio_account_sid}&
    env[TWILIO_APPLICATION_SID]={twilio_message_service_sid}&
    env[TWILIO_AUTH_TOKEN]={twilio_auth_token}&
    env[TWILIO_MESSAGE_SERVICE_SID]={twilio_message_service_sid}&
    env[TWILIO_STATUS_CALLBACK_URL]=https://{heroku_base_url}/twilio-message-report&
    env[PHONE_NUMBER_COUNTRY]=AU&
    env[DST_REFERENCE_TIMEZONE]=Australia/Melbourne
    '''.format(**session).replace('\n','').replace(' ','')
    return render_template("deploy.html", deploy_url=deploy_url)


if __name__ == '__main__':
    app.debug = True
    app.run(host="0.0.0.0")

