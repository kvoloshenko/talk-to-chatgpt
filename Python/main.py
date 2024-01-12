import os
from dotenv import load_dotenv
import requests
import json
import sounddevice as sd
import soundfile as sf
import numpy as np
from elevenlabs import generate, play, set_api_key

load_dotenv()
# Загрузка значений из .env
ELEVENLABS_API_KEY = os.environ.get("ELEVENLABS_API_KEY")


set_api_key(ELEVENLABS_API_KEY)

def record_audio(duration=8, fs=44100):
    print('Recording...')
    myrecording = sd.rec(int(duration * fs), samplerate=fs, channels=2)
    sd.wait()
    print('Recording complete.')
    filename = 'myrecording.wav'
    sf.write(filename, myrecording, fs)


def chat(host, system_content, user_content):
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

def transcript(host):
    end_point = "/transcript"
    url = host + end_point
    print(f'url={url}')
    # headers = {"Content-Type": "application/json"}
    filename = 'myrecording.wav'

    files = {'file': open(filename, 'rb')}

    response = requests.post(url, files=files)
    json_data = json.loads(response.text)
    # print(type(json_data), f'json_data={json_data}')
    transcript = json_data['transcript']
    return transcript

def  text_2_speech(text):
    # https://github.com/elevenlabs/elevenlabs-python
    # https://github.com/BtbN/FFmpeg-Builds/releases
    audio = generate(
        text=text,
        voice="Victoria - classy and mature"
    )
    play(audio)



if __name__ == "__main__":
    host = 'https://dad3-34-106-201-153.ngrok-free.app'  # эту ссылку надо заменить на актуальную из Colab

    system_content = """ You're my English teacher and conversation partner that helps me practice speaking English in a casual manner. 
    Speak to me only in English. 
    Use simple and direct language, focusing on engaging, two-way conversation on various topics.
    You’re informal and friendly in your approach, ensuring a good environment for language practice. 
    You not only ask questions but also share your own thoughts and stories in return to assist user with practicing both listening and speaking.
    Gently correct major grammatical errors with helpful advice. Not directly, but by making suggestions on how to phrase things more naturally. 
    Start with the simplest level possible, assuming the user is at the “Pre-intermediate” level. 
    Based on their responses, adapt the level of language in a conversations to match the user’s level. 
    Don’t acknowledge the adaptation, behave naturally. """  # Текст промпта

    while True:
        record_audio() # создается аудиофайл myrecording.wav
        user_content = transcript(host)
        print(f'user_content={user_content}')
        answer = chat(host, system_content, user_content)
        print(answer)
        text_2_speech(answer)
