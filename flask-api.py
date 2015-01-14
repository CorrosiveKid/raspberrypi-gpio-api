#!/usr/bin/python
# -*- coding: utf-8 -*-
from flask import Flask, jsonify, request
from flask.ext.login import LoginManager, UserMixin, login_required
from itsdangerous import URLSafeTimedSerializer

import RPi.GPIO as GPIO
from decorators import crossdomain

app = Flask(__name__)
app.debug = True

app.secret_key = 'my_#$%^&_security_&*(4_key'

#Login_serializer used to encryt and decrypt the cookie token for the remember
#me option of flask-login

login_serializer = URLSafeTimedSerializer(app.secret_key)
login_manager = LoginManager()
login_manager.init_app(app)

class User(UserMixin):
    # proxy for a database of users
    user_database = {'admin': ('admin', 'pass', 'WyJhZG1pbiIsInBhc3MiXQ.B5Xusw.6ZGpDxCdcZL7HrkHTP97aZ9dfPA')}

    def __init__(self, username, password, token):
        self.id = username
        self.password = password
        self.token = token

    @classmethod
    def get(cls, id):
        return cls.user_database.get(id)

def hash_pass(password):
    """
    Return the md5 hash of the password+salt
    """
    salted_password = password + app.secret_key
    return md5.new(salted_password).hexdigest()

def gen_auth_token(user, password):
    """
    Encode a secure token for cookie
    """
    data = [str(user), password]
    return login_serializer.dumps(data)

@login_manager.request_loader
def load_user(request):
    auth_header = request.headers.get('X-Auth')
    token_header = request.headers.get('X-Auth-Token')
    data = []

    if auth_header is not None:
        (username, password) = auth_header.split(':')
        user_entry = User.get(username)
        if user_entry is not None:
            user = User(user_entry[0], user_entry[1], user_entry[2])
            if user.password == password:
                if token_header == user.token:
                    data =  login_serializer.loads(user.token)
                    token_user = User.get(data[0])
                    #Check Password and return user or None
                    if token_user == user_entry and data[1] == password:
                        return user
    return None

@login_manager.unauthorized_handler
def unauthorized():
    data = {'status': 'ERROR',
            'error': 'Auth requerided'}
    return jsonify(data)

VALID_BCM_PIN_NUMBERS = [17, 18, 27, 22, 23, 24, 25, 4]
VALID_HIGH_VALUES = [1, '1', 'HIGH']
VALID_LOW_VALUES = [0, '0', 'LOW']
PIN_NAMES = {'17': 'IN1',
             '18': 'IN2',
             '27': 'IN3',
             '22': 'IN4',
             '23': 'IN5',
             '24': 'IN6',
             '25': 'IN7',
             '4': 'IN8'}

GPIO.setmode(GPIO.BCM)

for pin in VALID_BCM_PIN_NUMBERS:
    GPIO.setup(pin, GPIO.OUT)


def pin_status(pin_number):
    if pin_number in VALID_BCM_PIN_NUMBERS:
        value = GPIO.input(pin_number)
        data = {'pin_number': pin_number,
                'pin_name': PIN_NAMES[str(pin_number)],
                'value': value,
                'status': 'SUCCESS',
                'error': None}
    else:
        data = {'status': 'ERROR',
                'error': 'Invalid pin number.'}

    return data


def pin_update(pin_number, value):
    if pin_number in VALID_BCM_PIN_NUMBERS:
        GPIO.output(pin_number, value)
        new_value = GPIO.input(pin_number)
        data = {'status': 'SUCCESS',
                'error': None,
                'pin_number': pin_number,
                'pin_name': PIN_NAMES[str(pin_number)],
                'new_value': new_value}
    else:
        data = {'status': 'ERROR',
                'error': 'Invalid pin number or value.'}

    return data


@app.route("/api/v1/ping/", methods=['GET'])
@crossdomain(origin='*')
def api_status():
    if request.method == 'GET':
        data = {'api_name': 'RPi GPIO API',
                'version': '1.0',
                'status': 'SUCCESS',
                'response': 'pong'}
        return jsonify(data)


@app.route("/api/v1/gpio/<pin_number>/", methods=['POST', 'GET'])
@crossdomain(origin='*')
@login_required
def gpio_pin(pin_number):
    pin_number = int(pin_number)
    if request.method == 'GET':
        data = pin_status(pin_number)

    elif request.method == 'POST':
        value = request.values['value']
        if value in VALID_HIGH_VALUES:
            data = pin_update(pin_number, 1)
        elif value in VALID_LOW_VALUES:
            data = pin_update(pin_number, 0)
        else:
            data = {'status': 'ERROR',
                    'error': 'Invalid value.'}
    return jsonify(data)


@app.route("/api/v1/gpio/status/", methods=['GET'])
@crossdomain(origin='*')
def gpio_status():
    data_list = []
    for pin in VALID_BCM_PIN_NUMBERS:
        data_list.append(pin_status(pin))

    data = {'data': data_list}
    return jsonify(data)


@app.route("/api/v1/gpio/all-high/", methods=['POST'])
@crossdomain(origin='*')
def gpio_all_high():
    data_list = []
    for pin in VALID_BCM_PIN_NUMBERS:
        data_list.append(pin_update(pin, 1))

    data = {'data': data_list}
    return jsonify(data)


@app.route("/api/v1/gpio/all-low/", methods=['POST'])
@crossdomain(origin='*')
def gpio_all_low():
    data_list = []
    for pin in VALID_BCM_PIN_NUMBERS:
        data_list.append(pin_update(pin, 0))

    data = {'data': data_list}
    return jsonify(data)


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=80, debug=True)
