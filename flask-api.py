from flask import Flask, jsonify, request
import RPi.GPIO as GPIO

app = Flask(__name__)

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
def api_status():
    if request.method == 'GET':
        data = {'api_name': 'RPi GPIO API',
                'version': '1.0',
                'status': 'SUCCESS',
                'response': 'pong'}
        return jsonify(data)


@app.route("/api/v1/gpio/<pin_number>/", methods=['POST', 'GET'])
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
def gpio_status():
    data_list = []
    for pin in VALID_BCM_PIN_NUMBERS:
        data_list.append(pin_status(pin))

    data = {'data': data_list}
    return jsonify(data)


@app.route("/api/v1/gpio/all-high/", methods=['POST'])
def gpio_all_high():
    data_list = []
    for pin in VALID_BCM_PIN_NUMBERS:
        data_list.append(pin_update(pin, 1))

    data = {'data': data_list}
    return jsonify(data)


@app.route("/api/v1/gpio/all-low/", methods=['POST'])
def gpio_all_low():
    data_list = []
    for pin in VALID_BCM_PIN_NUMBERS:
        data_list.append(pin_update(pin, 0))

    data = {'data': data_list}
    return jsonify(data)


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=80, debug=True)