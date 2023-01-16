import socket
import threading
import time
import mysql.connector
import time
import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BOARD)
GPIO.setup(3, GPIO.OUT)
pwm=GPIO.PWM(3, 50)
pwm.start(0)

db = mysql.connector.connect(
  host="localhost",
  user="admin",
  passwd="admin",
  database="experiment"
)

cursor = db.cursor()

def SetAngle(angle):
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(3, GPIO.OUT)
    duty = angle / 18 + 2
    GPIO.output(3, True)
    pwm.ChangeDutyCycle(duty)
    time.sleep(1)
    GPIO.output(3, False)
    pwm.ChangeDutyCycle(0)

def function(conn, addr):
    try:
        while True:
            message = conn.recv(1024).decode()
            cursor.execute("Select id, name FROM users WHERE rfid_uid="+ message)
            result = cursor.fetchone()
            
            if cursor.rowcount >= 1:
                print("Authenticated")
                print("Welcome " + result[1])
                SetAngle(90)
                print("Gate Opened")
                message = (message + " Welcome " + result[1])
                
                cursor.execute("INSERT INTO attendance (user_id) VALUES (%s)", (result[0],) )
                db.commit()
                conn.send(message.encode())
                
                
            else:
                message = "User does not exist"
                conn.send(message.encode())
        conn.close()
    except Exception as e:
        conn.close()
    
    
s = socket.socket()         

port = 9696

s.bind(('', port))        
s.listen(5)
print("Server started")

while True:
    conn, addr  = s.accept()
    threading.Thread(target=function, args=(conn, addr)).start()

s.close()

