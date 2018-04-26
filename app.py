from flask import Flask, flash, session, render_template, request, redirect, url_for
from flask_session import Session
import requests

app = Flask(__name__)
SESSION_TYPE = 'filesystem'
app.config.from_object(__name__)
Session(app)

app.debug = True
app.secret_key = "q9283jrisadjfklasdfoqiwe82934u329sdf"


@app.route('/', methods=['GET', 'POST'])
def index():
    session['steps'] = 99
    # What do you want to call your app?
    # Validation rules: lowercase, alphanum, dashes ok, underscores not
    return render_template("index.html")


@app.route('/check_heroku_name', methods=['POST'])
def check_heroku_name():
    desired_url = "https://api.heroku.com/apps/{}".format(request.form[
                                                          'app_name'])
    headers = {'Content-type': 'application/json',
               'Accept': 'application/vnd.heroku+json; version=3'}
    session['name_available'] = (requests.get(
        desired_url, headers=headers).json()['id'] == 'not_found')

    if session['name_available']:
        flash('Your Heroku Name is available!')
        return redirect(url_for('create_heroku_account'))

    else:
        app_name_already_taken_message = 'Sorry, the name {} is already taken'.format(
            request.form['app_name'])
        flash(app_name_already_taken_message)
        return redirect(url_for('index'))


@app.route('/create_heroku_account')
def create_heroku_account():
    #Get the user to sign up for Heroku - No API for this
    return render_template("heroku.html")


@app.route('/create_authzero_account')
def create_authzero_account():
    #Get the user to sign up for Auth0 - No API for this
    #Walk the user through creating an API key / token
    return()


@app.route('/create_authzero_application')
def create_authzero_application():
    #Create a new client application
        #Params are Callback, Logout, CORS, Web Origins, OIDC Off
    #Save Domain Name, Client ID, Client Secret from response
    #Create Auth0 rule
    return()


@app.route('/create_twilio_account')
def create_twilio_account():
    #Get the user to sign up for Twilio - No API for this
    return()


@app.route('/create_twilio_application')
def create_twilio_application():
    #Collect the User's account Sid, Message Service Sid, Auth Token
    #Create a Twilio Messaging Service https://www.twilio.com/docs/sms/services/api#create-a-service
        # Params: Process Inbound Messages, Inbound Request URL, Status Callback URL
    # Collect account_sid, sid
    # From somewhere else? collect Twilio auth token
    # Purchase a Twilio number and tell the user what it is
    return()


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
