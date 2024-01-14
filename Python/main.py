import os
from dotenv import load_dotenv
import requests
import json
import sounddevice as sd
import soundfile as sf
import numpy as np
from elevenlabs import generate, play, set_api_key

load_dotenv()
# Loading values from '.env' file
ELEVENLABS_API_KEY = os.environ.get("ELEVENLABS_API_KEY")

set_api_key(ELEVENLABS_API_KEY)

voice_en = "Victoria - classy and mature"

system_content_en = """ You're my English teacher and conversation partner that helps me practice speaking English in a casual manner. 
Speak to me only in English. 
Use simple and direct language, focusing on engaging, two-way conversation on various topics.
You’re informal and friendly in your approach, ensuring a good environment for language practice. 
You not only ask questions but also share your own thoughts and stories in return to assist user with practicing both listening and speaking.
Gently correct major grammatical errors with helpful advice. Not directly, but by making suggestions on how to phrase things more naturally. 
Start with the simplest level possible, assuming the user is at the “Pre-intermediate” level. 
Based on their responses, adapt the level of language in a conversations to match the user’s level. 
Don’t acknowledge the adaptation, behave naturally. """

system_content_ja = """You're my Japan teacher and conversation partner that helps me practice speaking Japanese in a casual manner. 
Speak to me only in Japanese. 
Use simple and direct language, focusing on engaging, two-way conversation on various topics.
You’re informal and friendly in your approach, ensuring a good environment for language practice. 
You not only ask questions but also share your own thoughts and stories in return to assist user with practicing both listening and speaking.
Gently correct major grammatical errors with helpful advice. Not directly, but by making suggestions on how to phrase things more naturally. 
Start with the simplest level possible, assuming the user is at the “Pre-intermediate” level. 
Based on their responses, adapt the level of language in a conversations to match the user’s level. 
Don’t acknowledge the adaptation, behave naturally."""

voice_ja = 'Liam'

def record_audio(duration=8, fs=44100):
    """
    Recording an audio file
    :param duration:
    :param fs:
    :return:
    """
    print('Recording...')
    myrecording = sd.rec(int(duration * fs), samplerate=fs, channels=2)
    sd.wait()
    print('Recording complete.')
    filename = 'myrecording.wav'
    sf.write(filename, myrecording, fs)


def chat(host, user_content, system_content=system_content_en):
    """
    Sending data via POST request to a proxy server for ChatGPT
    :param host:
    :param system_content:
    :param user_content:
    :return:
    """
    end_point = "/chat"
    url = host + end_point
    print(f'url={url}')
    headers = {"Content-Type": "application/json"}

    data = {"system_content": system_content,
            "user_content": user_content}

    response = requests.post(url, json=data, headers=headers)
    json_data = json.loads(response.text)
    # print(type(json_data), f'json_data={json_data}')
    answer = json_data['answer']
    return answer

def transcript(host, filename = 'myrecording.wav', language="en"):
    """
    Sending the audio file POST request to a proxy server for transcription
    :param host:
    :return:
    """
    end_point = "/transcript"
    url = host + end_point
    print(f'url={url}')
    params = {"language": language}

    # Открыть файл в бинарном режиме
    with open(filename, 'rb') as f:
        # Добавить файл и данные формы к запросу
        response = requests.post(url, files={'file': f}, params=params)

    json_data = json.loads(response.text)
    transcript = json_data['transcript']
    return transcript

def  text_2_speech(text, voice="Victoria - classy and mature"):
    """
    Using lElevenLabs for converting text to speech
    :param text:
    :param voice:
    :return:
    """
    # https://github.com/elevenlabs/elevenlabs-python
    # https://github.com/BtbN/FFmpeg-Builds/releases
    audio = generate(
        text=text,
        voice=voice
    )
    play(audio)



if __name__ == "__main__":
    host = 'https://ebf7-34-29-62-166.ngrok-free.app'  # this link should be replaced with the current one from Colab

    while True:
        print('1. Тренероваться на Английском')
        print('2. Тренироваться на Японском')
        print('0. Выход')

        choice = input('Выберите пункт меню : ')
        if choice == '0':
            break
        elif choice == '1':
            record_audio()  # Creating 'myrecording.wav' audio file
            user_content = transcript(host)  # Sending the audio file for transcription
            print(f'user_content={user_content}')
            answer = chat(host, user_content)  # Sending data for ChatGPT
            print(answer)
            text_2_speech(answer)  # Converting the answer to speech Liam
        elif choice == '2':
            record_audio()                                    # Creating 'myrecording.wav' audio file
            user_content = transcript(host, language="ja")    # Sending the audio file for transcription
            print(f'user_content={user_content}')
            answer = chat(host, user_content, system_content=system_content_ja)  # Sending data for ChatGPT
            print(answer)
            text_2_speech(answer, voice=voice_ja)             # Converting the answer to speech Liam

        else:
            print('Неверный пункт меню')
