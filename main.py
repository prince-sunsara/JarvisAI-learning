from openai import OpenAI
import speech_recognition as sr
import win32com.client
import webbrowser
from config import OPENAI_API_KEY

speaker = win32com.client.Dispatch("SAPI.SpVoice")

def say(text):
    speaker.Speak(text)

def takeCommand():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print('Listening....')
        audio_data = r.listen(source)
        try:
            query = r.recognize_google(audio_data, language="en-IN")
            print(f"User said : {query}")
            return query
        except Exception as e:
            return "Some Error occured, Sorry."

def ai(prompt):
    text = f"Openai response from Prompt : {prompt}\n ************************** \n **************************\n\n"

    client = OpenAI(
        api_key=OPENAI_API_KEY
    )

    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "user", "content": prompt},
        ],
        top_p=1,
        max_tokens=256,
        temperature=0.7,
        frequency_penalty=0,
        presence_penalty=0
    )

    # print(response.choices[0].message)
    text += response.choices[0].message.content

    if not os.path.exists("Openai"):
        os.mkdir("Openai")

    with open(f"Openai/{''.join(prompt.split('intelligence')[1:30])}.txt", "w") as f:
        f.write(text)

# chatStr = ''
def chat(query):
    global chatStr
    client = OpenAI(
        api_key=OPENAI_API_KEY
    )

    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "user", "content": f'User: {query}\n'},
        ],
        top_p=1,
        max_tokens=256,
        temperature=0.7,
        frequency_penalty=0,
        presence_penalty=0
    )
    # chatStr += f'\nUser: {query}\n\nJarvis: {response.choices[0].message.content}'
    # print(chatStr)
    say(response.choices[0].message.content)
    return response.choices[0].message.content

if __name__ == '__main__':
    print('PyCharm')
    say("Hello, I am Jarvis A.I.")
    while True:
        query = takeCommand()
        sites = [['youtube','https://youtube.com'], ['wikipedia','https://wikipedia.com'],['instagram','https://instagram.com'],['facebook','https://facebook.com'],['google','https://google.com']]
        for site in sites:
            if f'Open {site[0]}'.lower() in query.lower():
                say(f"Opening {site[0]}...")
                webbrowser.open(site[1])
        # say(query)
        if 'open music' in query:
            import vlc
            player = vlc.MediaPlayer("F:/m/1/13-DHOON.mp3")
            player.play()

        elif 'the time' in query:
            import datetime
            h = datetime.datetime.now().strftime("%H")
            m = datetime.datetime.now().strftime("%M")
            say(f"The time is {h} hour {m} minutes")

        elif "open notepad".lower() in query.lower():
            import os
            os.system("notepad.exe")

        elif 'Using Artificial Intelligence'.lower() in query.lower():
            ai(prompt=query)

        elif "jarvis quit".lower() in query.lower():
            exit()

        else:
            chat(query)