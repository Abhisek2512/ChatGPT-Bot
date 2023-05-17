import openai
import pyttsx3
import speech_recognition as sr
import pywhatkit
import datetime
import wikipedia
import pyjokes
import logging

openai.api_key = "your_api_key"

engine = pyttsx3.init()
hello_said = False
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id)

def transcribe_audio_to_text(filename):
    recognizer = sr.Recognizer()
    with sr.AudioFile(filename) as source:
        audio = recognizer.record(source)
    try:
        return recognizer.recognize_google(audio)
    except:
        speak_text('Error transcribing audio')

def generate_response(prompt):
    response = openai.Completion.create(
          engine="text-davinci-002",
        prompt=prompt,
        temperature=0.7,
        max_tokens=1024,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0
    )
    return response.choices[0].text.strip()

def speak_text(text): 
    engine.say(text)
    engine.runAndWait()

logging.basicConfig(filename='bot.log', level=logging.ERROR)

def send_message():
    recognizer = sr.Recognizer()

    speak_text('Whom should I send message to?')
    with sr.Microphone() as source:
        speak_text('Listening...')
        recognizer.pause_threshold = 1
        voice = recognizer.listen(source)
        contact_name = recognizer.recognize_google(voice)
        speak_text(f'You said: {contact_name}')

        # search for the contact's phone number in your contacts
        contacts = {
            'Abhishek': '+917378488815',
                      
            # add more contacts here
        }

        if contact_name in contacts:
            now = datetime.datetime.now()
            hour = now.hour
            minute = now.minute
            speak_text("Tell me a message")
            recognizer.pause_threshold = 1
            voice = recognizer.listen(source)
            message = recognizer.recognize_google(voice)
            speak_text(message)
            pywhatkit.sendwhatmsg(contacts[contact_name], message, hour, (minute+2))
            speak_text(f'Message sent to {contact_name} successfully!')
        else:
            speak_text(f"{contact_name} not found in your contacts. Please try again!")



def main():
    global hello_said
    while True:
        try:
            if not hello_said:
                speak_text("Say 'hello' to start recording your question...")
                with sr.Microphone() as source:
                    recognizer = sr.Recognizer()
                    audio = recognizer.listen(source)
                    try:
                        transcription = recognizer.recognize_google(audio)
                        if transcription.lower() == "hello":
                            hello_said = True
                            # print("You said: hello")
                            speak_text("Say your question...")
                    except sr.UnknownValueError:
                        speak_text("Could not understand audio")
                    except sr.RequestError as e:
                        speak_text(f"Error with speech recognition service: {e}")
            else:
                with sr.Microphone() as source:
                    recognizer = sr.Recognizer()
                    audio = recognizer.listen(source)
                    try:
                        filename = "input.wav"
                        with open(filename, "wb") as f:
                            f.write(audio.get_wav_data())
                        text = transcribe_audio_to_text(filename)
                        if text is not None and any(val in text for val in ['send message','who is','time', 'tell', 'play','joke','email to']):

                            if 'email to' in text:
                                speak_text('Tell me the subject of the email')
                                with sr.Microphone() as source:
                                        speak_text('Listening...')
                                        recognizer.pause_threshold = 1
                                        voice = recognizer.listen(source)
                                        subject = recognizer.recognize_google(voice)
                                        speak_text(f'You said: {subject}')

                                email_body = generate_response(subject)
                                print(email_body)
                                speak_text(email_body)


                            if 'send message' in text:
                                send_message()                                
                                
                            if 'time' in text: 
                                time= datetime.datetime.now().strftime('%I:%M %p')
                                speak_text(time)
                                
                            if 'tell' in text:
                                tell = 'Hello there! I am Sarthi , an intelligent software application designed by Abhishek Nashirkar, a skilled electrical engineer at Bajaj Institute of Technology. I am here to assist you with various tasks and make your life easier. My advanced algorithms and natural language processing capabilities enable me to understand and respond to human language, making me a powerful tool for automating and streamlining various processes.'
                                speak_text(tell)

                            if 'play' in text:
                                video = text.replace('play', '')
                                speak_text('playing....'+ video)
                                pywhatkit.playonyt(video)

                            if 'joke' in text:
                                speak_text(pyjokes.get_joke())

                            if 'who is' in text:
                                person = text.replace('who is', '')
                                info = wikipedia.summary(person, 1)
                                speak_text(info)

                           
                        elif text is not None:
                            response = generate_response(text)
                            print(f"Sarthi: {response}")
                            speak_text(response)

                        else:
                            speak_text("Error transcribing audio, repeat your question")
                            
                    except sr.UnknownValueError:
                        speak_text(logging.error("Sorry, I couldn't understand what you said. Please try again."))
                    except sr.RequestError as e:
                        speak_text(logging.error(f"Sorry, there was an error with the speech recognition service. Please try again."))
        except Exception as e:
            print(f"An error occurred: {str(e)}")
            print("Soory, something went wrong. Please try again.")
            continue

if __name__ == "__main__":
    main()
 
