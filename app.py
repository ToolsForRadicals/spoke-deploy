import flask
from flask_session import Session

app = flask.Flask(__name__)
SESSION_TYPE = 'filesystem'
app.config.from_object(__name__)
Session(app)

app.debug = True
app.secret_key = "q9283jrisadjfklasdfoqiwe82934u329sdf"


@app.route('/')
def index():
    # What do you want to call your app?
    return()

@app.route('/check_heroku_name', methods=['POST'])
def check_heroku_name():
    #Check to see if the heroku name is available
    # TODO: Reserve it somehow during this process?
    return()

@app.route('/create_heroku_account')
def create_heroku_account():
    #Get the user to sign up for Heroku - No API for this
    return()

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











# TODO

## 

## Do you already have any of the following?
* Heroku Account
* Twilio Account
* Auth0 Account

## Create Heroku account
    * Check app name is available on Heroku

## Create Auth0 account
    * Create Auth0 Application
        * Set Callback, Logout, CORS, Web Origins
        * Collect Domain name, Client ID, Client Secret
        * Set OIDC Conformant Off
        * Create a rule in Auth0

## Create Twilio account
    * Create a new Messaging Service
    * Enable Process Inbound Messages
        * Add Inbound Request URL
    * Add Outbound Status Callback URL
    * Collect Twilio Account SID (API Key), Twilio Message Service ID (Twilio Application ID), and Twilio Auth Token
    * Purchase a Twilio Phone number (or provide a popup to remind the user to do it)

## Create a Heroku Deploy button

## Done



if __name__ == '__main__':
    app.run()