import RPi.GPIO as GPIO

def init():
	print('Initializing GPIO output pins')
	GPIO.setmode(GPIO.BCM)
	GPIO.setup(17, GPIO.OUT)
	GPIO.setup(18, GPIO.OUT)
	GPIO.setup(27, GPIO.OUT)
	GPIO.setup(22, GPIO.OUT)
	GPIO.setup(23, GPIO.OUT)
	GPIO.setup(24, GPIO.OUT)
	GPIO.setup(25, GPIO.OUT)
	GPIO.setup(4, GPIO.OUT)
	print('Success!')

def switch_on(pins):
	for pin in pins:
		print ('Switching on pin %s' % pin)
		GPIO.input(pin, 1)


def switch_off(pins):
	for pin in pins:
		print ('Switching off pin %s' % pin)
		GPIO.input(pin, 0)

	
def status(pin):
	print('%s', GPIO.output(pin))


def main():
	init()
	
if __name__ == '__main__':
	main()


