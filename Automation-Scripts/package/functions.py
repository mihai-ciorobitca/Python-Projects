import pyttsx3, psutil, shutil
import os, sys, win32api, qrcode
from cryptography.fernet import Fernet
import pyautogui, time

engine = pyttsx3.init()
engine.setProperty('rate', 120)

def speak(text):
    engine.say(text)
    engine.runAndWait()

def alarm():
    level = 20
    while True:
        batery = psutil.sensors_battery()
        if batery.percent < level and not\
           batery.power_plugged:
           speak(f'Battery is {batery.percent} percent, plug in!')
            
def encrypt():
    list_files = os.listdir("input")
    key = Fernet.generate_key()
    with open("key.key", "wb") as the_key:
        the_key.write(key)
    for file in list_files:
        with open(f'input/{file}', 'rb') as f:
            content = f.read()
        files_content = Fernet(key).encrypt(content)
        with open(f'input/{file}', "wb") as f:
            f.write(files_content)
    print('Files encrypted!')

def decrypt():
    list_files = os.listdir("input")                                     #load files
    if os.path.isfile('./key.key'):                                      #check key
        with open('./key.key', 'rb') as file:
            key = file.read()
        for file in list_files:
            with open(f'input/{file}', 'rb') as f:
                continut = f.read()
            try:
                continut_decriptat = Fernet(key).decrypt(continut)      #try to decrypt
            except:
                print('Invalid key')
            with open(f'input/{file}', "wb") as f:
                f.write(continut_decriptat)
        print('Fisierele au fost decriptate')
    else:
        print('Key not found') 

def qr():
    with open('input.txt', 'r') as file:
        images = file.readlines()
    images = [image.split(' ') for image in images]
    for image in images:
        qr = qrcode.make(image[1])
        qr.save(f"./output/{image[0]}.jpg")   

def detect_movement():
    (x_mouse, y_mouse) = win32api.GetCursorPos()
    while True:
        if win32api.GetCursorPos() != (x_mouse, y_mouse):
            speak("Don't touch my laptop!")
        if os.path.exists('alarm.txt'):
            break  

def screenshot():
    index = 0
    interval = input("Set interval in seconds: ")
    while True:
        camera = pyautogui.screenshot()
        camera.save(f'output/{index + 1}.png')  
        index += 1
        time.sleep(interval)    