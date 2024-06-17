import Transcription
import Ollama
import time
import threading


context = []
def add_context(role, content):
    context.append({'role': role, 'content': content})

def voice_instruct():
    while True:
        voice_instruct = Transcription.transcribe_return()
        add_context('user', voice_instruct)

def ollama():
    while True:
        response = Ollama.stream_responses(context)
        add_context('assistant', response)

def call_response():
    voice_instruct()
    ollama()

listen_thread = threading.Thread(target=voice_instruct)
respond_thread = threading.Thread(target=ollama)

listen_thread.start()
respond_thread.start()

while True:
    time.sleep(1)