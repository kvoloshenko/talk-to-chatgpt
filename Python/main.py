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


def chat(host, system_content, user_content):
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

def transcript(host):
    """
    Sending the audio file POST request to a proxy server for transcription
    :param host:
    :return:
    """
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
    """
    Using lElevenLabs for converting text to speech
    :param text:
    :return:
    """
    # https://github.com/elevenlabs/elevenlabs-python
    # https://github.com/BtbN/FFmpeg-Builds/releases
    audio = generate(
        text=text,
        voice="Victoria - classy and mature"
    )
    play(audio)



if __name__ == "__main__":
    host = 'https://8939-34-74-114-234.ngrok-free.app'  # this link should be replaced with the current one from Colab

    system_content = """ You're my English teacher and conversation partner that helps me practice speaking English in a casual manner. 
    Speak to me only in English. 
    Use simple and direct language, focusing on engaging, two-way conversation on various topics.
    You’re informal and friendly in your approach, ensuring a good environment for language practice. 
    You not only ask questions but also share your own thoughts and stories in return to assist user with practicing both listening and speaking.
    Gently correct major grammatical errors with helpful advice. Not directly, but by making suggestions on how to phrase things more naturally. 
    Start with the simplest level possible, assuming the user is at the “Pre-intermediate” level. 
    Based on their responses, adapt the level of language in a conversations to match the user’s level. 
    Don’t acknowledge the adaptation, behave naturally. """  # Prompt text

    while True:
        record_audio()                                    # Creating 'myrecording.wav' audio file
        user_content = transcript(host)                   # Sending the audio file for transcription
        print(f'user_content={user_content}')
        answer = chat(host, system_content, user_content) # Sending data for ChatGPT
        print(answer)
        text_2_speech(answer)                             # Converting the answer to speech
