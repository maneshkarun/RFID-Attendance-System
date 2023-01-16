import socket
import threading
import time
import RPi.GPIO as GPIO
from mfrc522 import SimpleMFRC522

GPIO.setmode(GPIO.BOARD)
GPIO.setup(3, GPIO.OUT)
pwm=GPIO.PWM(3, 50)
pwm.start(0)

def SetAngle(angle):
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(3, GPIO.OUT)
    duty = angle / 18 + 2
    GPIO.output(3, True)
    pwm.ChangeDutyCycle(duty)
    time.sleep(1)
    GPIO.output(3, False)
    pwm.ChangeDutyCycle(0)
    
ir1_sensor = 16
ir2_sensor = 40

GPIO.setmode(GPIO.BOARD)
GPIO.setup(ir1_sensor,GPIO.IN)
GPIO.setup(ir2_sensor,GPIO.IN)

print ("IR Sensor Ready")

reader = SimpleMFRC522()

port = 9696
s = socket.socket() 
s.connect(('', port))
print("Client Connected.")


try: 
   while True:
        
        ir1_state = GPIO.input(ir1_sensor)
        if (ir1_state == 0):
             print ("Object Detected")     
          #RFID code
             print('Place Card to record attendance')
             id, text = reader.read()
             
             message = str(id)
             
             s.send(message.encode())
             message = s.recv(1024).decode()  
             print(message)
             time.sleep(2)
             ir2_state = GPIO.input(ir2_sensor)
             if (ir2_state == 0):
                 SetAngle(0)
                 print("Door closed")
             else:
                 SetAngle(0)
        else:
             s.close


except KeyboardInterrupt:
    GPIO.cleanup()



