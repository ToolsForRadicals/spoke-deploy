# Spoke Deploy

An app to automatically deploy Spoke(https://opensource.moveon.org/spoke/) to Heroku for you.

## Getting Started

You can deploy this app to Heroku too:
[![Deploy](https://www.herokucdn.com/deploy/button.svg)](https://heroku.com/deploy)

Or you can use the one at https://spokedeploy.herokuapp.com

## What does it do?

Spoke Deploy helps you collect the info you need to set up Spoke, the P2P texting app. It also configures your Auth0 and Twilio accounts automatically for Spoke. 
When you're finished, you'll have a one-click ready to deploy Spoke app that your supporters and campaigners can start using right away.


### Prerequisites

During Deployment, you'll need to sign up for an account with Auth0 and Twilio. You'll also need to add at least $20 to your Twilio account in order to start texting.

## Built With

* [Flask](http://flask.pocoo.org) - The web framework used


## TODO (Pull requests welcome!)
* Client side input validation
* Error / Exception handling for Twilio & Auth0 failures (With some kind and sensible error messages)
* A frontend design re-skin
* Basic test coverage

## Contributing

Contributions very welcome, pull requests welcome. Feedback on an actual deployment also welcome

## Authors

* **Anthony Mockler** - *Initial work* - [IAmCarbonatedMilk](https://iamcarbonatedmilk.com)