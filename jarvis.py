import pyttsx3
import datetime
import speech_recognition as sr
import wikipedia as wiki
import webbrowser
import urllib
import re
import random
import smtplib
import requests
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from jokes import jokesDict
from randomMusicList import randomMusicList
from emailDict import *
from smsDict import smsDict


engine = pyttsx3.init('sapi5')

voices= engine.getProperty('voices') #getting details of current voice

engine.setProperty('voices', voices[0].id) #changing index, changes voices. 1 for female

chrome_path = "C:/Program Files (x86)/Google/Chrome/Application/chrome.exe %s"      #State your chrome path


def speak(audio):
    engine.say(audio) 
    engine.runAndWait() #Without this command, speech will not be audible to us.



''' Wishes on startup according to hour '''

def wishMe():
    hour = datetime.datetime.now().hour
    
    if hour >= 5 and hour < 12 :
        speak("Good Morning ")

    elif hour >= 12 and hour <= 18:
        speak("Good Afternoon ")

    else :
        speak("Good evening")

    speak("I am Jarvis Sir. What can I do for you ?")


''' Take Command '''

def takeCommand():
    #It takes microphone input from the user and returns string output

    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        r.pause_threshold = 1
        r.energy_threshold = 300
        r.adjust_for_ambient_noise(source) #reduce noise
        audio = r.listen(source)
    
    try:
        print("Recognizing...")    
        query = r.recognize_google(audio, language='en-in') #Using google for voice recognition.
        print(f"You said: {query}\n")  #User query will be printed.

    except Exception as e:
        # print(e)    
        print("Say that again please...")   #Say that again will be printed in case of improper voice 
        return "None" #None string will be returned
    return query


''' Send email '''

def sendEmail(subject,to, content):
    #The mail addresses and password
    sender_address = 'yourEmail@gmail.com'
    sender_pass = 'your_password.'
    receiver_address = to
    #Setup the MIME
    message = MIMEMultipart()
    message['From'] = sender_address
    message['To'] = receiver_address
    message['Subject'] = subject   #The subject line

#For customised email
# getName(email_id) takes email id as argument and returns the name corresponding to the email id

    content = '''Hi ''' + getName(to) + ''',

How are you? ''' + content + '''.

Regards,
Abhinav Anand'''


    #The body and the attachments for the mail
    message.attach(MIMEText(content, 'plain'))

    #Create SMTP session for sending the mail
    session = smtplib.SMTP('smtp.gmail.com', 587) #use gmail with port
    session.starttls() #enable security
    session.login(sender_address, sender_pass) #login with mail_id and password
    text = message.as_string()
    session.sendmail(sender_address, receiver_address, text)
    session.quit()
    print('email sent to ' + getName(to))   


''' Send SMS '''
'''Used Fast2sms developer API
go to https://docs.fast2sms.com/ for reference '''

def sendSMS(to,content):
    url = "https://www.fast2sms.com/dev/bulk"

    content = '''From Abhinav :  
 ''' + content.capitalize()

    payload = "sender_id=FSTSMS&message=" + content + "&language=english&route=p&numbers=" + to
    headers = {
    'authorization': "GuTUEkoSX5shYKOlBHcvZDeAaJNrqbxigQ90tVwRyzdp14L28MCJeTnGLHAWZw1qv9zRE07XBFkYSjlc",
    'Content-Type': "application/x-www-form-urlencoded",
    'Cache-Control': "no-cache",
    }
    response = requests.request("POST", url, data=payload, headers=headers)
    print(response.text)

''' Main Function '''

if __name__=="__main__" :
    # speak("Hi Abhinav")
    wishMe()

    while True:
        query =  takeCommand().lower()

        if "wikipedia" in query:
           query = query.replace("wikipedia", "")
           speak("Searching wikipedia..")
           results = wiki.summary(query, sentences = 1)
           print(results)
           speak(results)
           speak("What else can I do Sir")


        elif "play" in query:
            search_keyword = query.replace(" ", "+").replace("play", "")
            html = urllib.request.urlopen("https://www.youtube.com/results?search_query=" + search_keyword)
            video_ids = re.findall(r"watch\?v=(\S{11})", html.read().decode())
            url = "https://www.youtube.com/watch?v=" + video_ids[0]

            reply = str(random.choices(randomMusicList))
            speak(reply)
            print(reply)
            
            webbrowser.get(chrome_path).open_new_tab(url)
        
        
        elif "open google" in query :
            url = "google.com"
            webbrowser.get(chrome_path).open_new_tab(url)
        
        
        elif "open youtube" in query :
            url = "youtube.com"
            webbrowser.get(chrome_path).open_new_tab(url)


        elif "search youtube" in query :
            query = query.replace("search youtube for", "").replace(" ", "+")
            url = "https://www.youtube.com/results?search_query=h" + query
            webbrowser.get(chrome_path).open_new_tab(url)


        elif  "search" in query :
            query = query.replace("search for ", "").replace(" ","+")
            query = query.replace(" ", "+")
            url = "https://www.google.com/search?q=" + query
            webbrowser.get(chrome_path).open_new_tab(url)


        elif "shop" in query :
            query = query.replace("shop for", "").replace("at amazon", "").replace(" ", "")
            url = "https://www.amazon.in/s?k=" + query
            webbrowser.get(chrome_path).open_new_tab(url)

        elif "text" in query or "message" in query or "sms" in query :
            try :
                name = query.replace("send","").replace(" a ", "").replace("text", "").replace("message","").replace("to", "").replace("sms", "").replace(" ","")
                speak("What should I say?")
                content = takeCommand()

                speak("Should I send it?")
                flag = takeCommand().lower()

                if flag == "no":
                    print("Message has been discarded")
                    speak("Message has been discarded")
                
                else :
                    to = smsDict[name]
                    sendSMS(to, content)
                    speak("Message has been sent")
                    print("Message has been sent")
            
            except Exception as e :
                print(e)
                speak("Sorry I couldn't send the text")
            
        
        elif 'email' in query or "mail" in query:
            try:
                name = query.replace("send", "").replace("email","").replace("mail", "").replace("to","").replace("an","").replace(" ","")
                speak("What should I put in subject?")
                subject = takeCommand()
                subject = subject.capitalize()
                speak("Okay, What should I say?")
                content = takeCommand()
                content = content.capitalize()
                
                speak("Should I send it ?")
                flag = takeCommand().lower()

                if flag =="no" :
                    speak("email has been discarded")
                    print("email has been discarded")

                else :
                    to = emailDict[name]
                    sendEmail(subject, to, content)
                    speak("email has been sent !")
               
            except Exception as e:
                print(e)
                speak("Sorry, I am not able to send this email")

        elif 'the time' in query:
            strTime = datetime.datetime.now().strftime("%H:%M:%S")    
            speak(f"Sir, the time is {strTime}")

        elif "joke" in query or "jokes" in query :
            joke = str(random.choices(jokesDict))
            print(joke)
            speak(joke)

        else :
            speak("I didn't get that. Please say that again")


            
