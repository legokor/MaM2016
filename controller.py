# coding=utf-8
#!/usr/bin/python

from pynput import keyboard
import serial

ser = serial.Serial("COM6")  # Itt kell módosítani a portot ( windows esetében COM%)
ser.baudrate = 9600

speed = 0.3 # 0 tól 0.5 ig

lastServoPos = 3000
servoPos = 3000

motorA = 0.5
motorB = 0.5
lastMotorA = 0.0
lastMotorB = 0.0

aktuator = [0,0,0,0]
pressed_keys = []

print("Kilépéshez nyomj Escape-t")
print("Iranyitas w,a,s,d")
print("Szervo q,e,r - kozep ")
print("Aktuator1 h,j ")
print("Aktuator2 k,l")

def send_commands(commands):
    global ser
    for command in commands:
        ser.write(command.encode())
        print (command)

def process_buttons():
    global motorA,motorB,lastMotorA,lastMotorB,servoPos,lastServoPos, pressed_keys, ser

    commands = []
    # Main motors
    if 'w' in pressed_keys:
        motorA = 0.5+speed
        motorB = 0.5+speed
    elif 's' in pressed_keys:
        motorA = 0.5-speed
        motorB = 0.5-speed
    elif 'a' in pressed_keys:
        motorA = 0.5+speed
        motorB = 0.5-speed
    elif 'd' in pressed_keys:
        motorA = 0.5-speed
        motorB = 0.5+speed
    else:
        if lastMotorA != 0 or lastMotorB != 0:
            motorA = 0.5
            motorB = 0.5
    if motorA != lastMotorA or motorB != lastMotorB:
        commands.append("$BigDcDutys,"+str(motorA)+","+str(motorB)+"*")
        lastMotorA = motorA
        lastMotorB = motorB

    # Szervo
    if 'q' in pressed_keys:
        servoPos = 4200
    elif 'e' in pressed_keys:
        servoPos = 3000
    elif 'r' in pressed_keys:
        servoPos = 3600
    
    if servoPos != lastServoPos:
        commands.append("$ServoPosition,"+str(servoPos)+"*")
        lastServoPos = servoPos


    # Aktuator 1
    if 'h' in pressed_keys:
        commands.append("$ActuatorM1Direction,1*")
    elif 'j' in pressed_keys:
        commands.append("$ActuatorM1Direction,2*")

    # Aktuator 2
    if 'k' in pressed_keys:
        commands.append("$ActuatorM2Direction,1*")
    elif 'l' in pressed_keys:
        commands.append("$ActuatorM2Direction,2*")
    return commands

def on_press(key):
    try:
        if key.char not in pressed_keys:
            pressed_keys.append(key.char)
        commands = process_buttons()
        send_commands(commands)
    except AttributeError:
        pass

def on_release(key):
    global ser
    try:
        pressed_keys.remove(key.char)
        if 'w' not in pressed_keys and 's' not in pressed_keys and 'd' not in pressed_keys and 'a' not in pressed_keys:
            motorA = 0.5
            motorB = 0.5
            commands = process_buttons()
            send_commands(commands)
    except AttributeError:
        pass
    # Stop Listener
    if key == keyboard.Key.esc:
        ser.close()
        return False

# Collect events until released
with keyboard.Listener(
        on_press=on_press,
        on_release=on_release) as listener:
    listener.join()
