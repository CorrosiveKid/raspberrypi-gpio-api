# Raspberry Pi GPIO API #

This is a simple RESTful API built with Python on Flask to control the GPIO pins of a Raspberry Pi. Please note that this application can only be run on a Raspberry Pi and the GPIO pin numbering is in BCM format.

## Getting Started ##

### Step 1 - Installing Pip ###
```shell
pi@raspberrypi ~ $ sudo apt-get install python-pip
```
### Step 2 - Installing Requirements ###
```shell
pi@raspberrypi ~ $ cd raspberrypi-gpio-api
pi@raspberrypi ~/raspberrypi-gpio-api $ sudo pip install -r requirements.txt

```
Above command should successfully install the required dependencies.
### Step 3 - Run the development web server ###
```shell
pi@raspberrypi ~/raspberrypi-gpio-api $ sudo python flask-api.py

```
That should start the development server up.
### Step 4 - Test the API ###
To test if the API is running properly, open up a browser and call the ping url of the API - **{{Your RPi IP Address}}/api/v1/ping/**

If the API is running properly, you should see something like this on your browser.
```
{
    'api_name': 'RPi GPIO API',
    'response': 'pong',
    'status': 'SUCCESS',
    'version': '1.0'
}
```
You're all set! :D

## API endpoints ##

** /api/v1/ping/ **

* Supported Methods - GET
* GET - Returns the status of the API.
* POST - Not supported.

** /api/v1/gpio/<pin_number>/ **

* Supported Methods - GET, POST
* GET - Returns the status of specified GPIO BCM pin number.
* POST - Sets the value for the specified GPIO pin.
    * Parameters supported
        * value (Valid values are 0 or 1)

** /api/v1/gpio/status/ **

* Supported Methods - GET
* GET - Returns the status all the GPIO pins.
* POST - Not supported.

** /api/v1/gpio/all-high/ **

* Supported Methods - POST
* GET - Not supported.
* POST - Sets the GPIO value to 1 on all the pins.

** /api/v1/gpio/all-low/ **

* Supported Methods - POST
* GET - Not supported.
* POST - Sets the GPIO value to 0 on all the pins.