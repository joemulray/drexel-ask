![drexel-ask logo](http://www.mulray.info/images/drexel-ask.png)

# drexel-ask

[![Build Status](https://travis-ci.org/joemulray/drexel-ask.svg?branch=master)](https://travis-ci.org/joemulray/drexel-ask)


### Prerequisites

* [ngrok](https://ngrok.com/download)
* python-pip
* Amazon Developer Account


### Installation

```
➜  ~ virtualenv .

source bin/activate
pip install -r requirements.txt
python app.py

```

* The default flask port will run on port 5000, if you change that port also change your ngrok port to tunnel to
```
➜  ~ ngrok http 5000

ngrok by @inconshreveable

Session Status                online
Session Expires               7 hours, 59 minutes
Version                       2.2.8
Region                        United States (us)
Web Interface                 http://127.0.0.1:4040
Forwarding                    http://96c94a4b.ngrok.io -> localhost:5000
Forwarding                    https://96c94a4b.ngrok.io -> localhost:5000

Connections                   ttl     opn     rt1     rt5     p50     p90
                              0       0       0.00    0.00    0.00    0.00
```

* You will use this url : `https://96c94a4b.ngrok.io` as your Default Region endpoint
* Select `My development endpoint is a sub-domain of a domain that has a wildcard certificate from a certificate authority`
* Bulk upload the sample utterances


### Features

* Class Schedule
* Next Class
* Next Semester
* Detailed Class information
* Daily rundown
* Refresh Account information

### Future Features

* Estimated travel time to class location

### Current Issues
* The token generated from dm1 api often expires and will unallow you to grab your class information, needs better handling in that envent, that token expires or fails to get user information.

### Acknoledgements
* Flask-Ask : library to enable Alexa to python connection
* Alexa Flask-ASK : library as addon to Flask-Ask to allow scenario based conversations

