from flask import Flask, flash, session, render_template, request, redirect, url_for
from flask_session import Session
import requests

app = Flask(__name__)
SESSION_TYPE = 'filesystem'
app.config.from_object(__name__)
Session(app)

app.debug = True
app.secret_key = "q9283jrisadjfklasdfoqiwe82934u329sdf"


def create_authzero_application(authzero_token):
    #Create a new client application
        #Params are Callback, Logout, CORS, Web Origins, OIDC Off
    #Save Domain Name, Client ID, Client Secret from response
    #Create Auth0 rule
    return()

def create_twilio_application(twilio_account_sid,twilio_auth_token):
    #Collect the User's account Sid, Message Service Sid, Auth Token
    #Create a Twilio Messaging Service https://www.twilio.com/docs/sms/services/api#create-a-service
        # Params: Process Inbound Messages, Inbound Request URL, Status Callback URL
    # Collect account_sid, sid
    # From somewhere else? collect Twilio auth token
    # Purchase a Twilio number and tell the user what it is
    return()

@app.route('/', methods=['GET', 'POST'])
def index():
    session['steps'] = 99
    return render_template("index.html")

@app.route('/steps')
def steps():
    return render_template("steps.html")

@app.route('/create_authzero_application')
def create_applications():
    session['authzero_token'] = request.form['authzero_token']
    session['twilio_account_sid'] = request.form['twilio_account_sid']
    session['twilio_auth_token'] = request.form['twilio_auth_token']
    try:
        authzero_result = create_authzero_application(session['authzero_token'])
        if authzero_result['success'] == True:
            print("Auth0 worked")
    except:
        flash("Couldn't create your Auth0 service. Double check your token?")
        return redirect(url_for("index"))
    try:
        twilio_result = create_twilio_application(session['twilio_account_sid'],session['twilio_auth_token'])
        if twilio_result['success'] == True:
            print("Twilio worked!")
    except:
        print("Something didn't work with Twilio")
    return

@app.route('/check_heroku_name', methods=['POST'])
def check_heroku_name():
    session['app_name'] = request.form['app_name']
    desired_url = "https://api.heroku.com/apps/{}".format(session[
                                                          'app_name'])
    headers = {'Content-type': 'application/json',
               'Accept': 'application/vnd.heroku+json; version=3'}
    session['name_available'] = (requests.get(
        desired_url, headers=headers).json()['id'] == 'not_found')

    if session['name_available']:
        flash('Your Heroku Name is available!')
        return redirect(url_for('steps'))

    else:
        app_name_already_taken_message = 'Sorry, the name {} is already taken'.format(
            request.form['app_name'])
        flash(app_name_already_taken_message)
        return redirect(url_for('index'))







@app.route('/deploy')
def create_heroku_deploy_button():
    params = dict()
    deploy_url = '''
    https://heroku.com/deploy?
    template={template}&
    [AUTH0_DOMAIN]={authzero_domain}&
    [AUTH0_CLIENT_ID]={authzero_client_id}&
    [AUTH0_CLIENT_SECRET]={authzero_client_secret}&
    [BASE_URL]={heroku_base_url}&
    [TWILIO_API_KEY]={twilio_account_sid}&
    [TWILIO_APPLICATION_SID]={twilio_message_service_sid}&
    [TWILIO_AUTH_TOKEN]={twilio_auth_token}&
    [TWILIO_MESSAGE_SERVICE_SID]={twilio_message_service_sid}&
    [TWILIO_STATUS_CALLBACK_URL]=https://{heroku_base_url}/twilio-message-report&
    [PHONE_NUMBER_COUNTRY]=AU&
    [DST_REFERENCE_TIMEZONE]=Australia/Sydney
    '''.format(**params)
    return(deploy_url)


if __name__ == '__main__':
    app.run(debug=True)
