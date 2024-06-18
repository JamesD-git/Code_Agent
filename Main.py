import Transcription
import Ollama
import time
import os
import concurrent.futures
from threading import Event


context = []
def add_context(role, content):
    context.append({'role': role, 'content': content})

def voice_instruct(event=None):
            voice_instruct = Transcription.transcribe_return(event)
            if len(str(voice_instruct)) > 1:
                add_context('user', voice_instruct)
                # print("NEW INSTRUCTIONS RECIEVED")
                return voice_instruct

def ollama(name):
    init_context = context.copy()
    gen = Ollama.stream_responses(init_context)
    response = ""
    while True:
        try:
            if context == init_context:
                token = next(gen)
                if len(token) > 0:
                    print(token, end="", flush=True)
                    # Add token to response
                    response += token
                    # OPTIONAL tts
                    # if token != "" and token != " " and token != "'" and token != "\n": 
                    #     os.system(f'say {token}')
                else:
                    continue
            else:
                 print("CONTEXT CHANGED")
                 add_context(name, response)
                 user_text = context.pop(-2)
                 context.append(user_text)
                 break
        except StopIteration:
            print('STOP ITERATION')
            add_context(name, response)
            event.set()
            return response
        
    
while context == []:
    # voice_instruct()
    add_context("user", "Let's do an extensive brainstorm on business ideas which I can start for $500 or less, and which may profit $10,000 in the first weekend of sales")
name = 'assistant'

while context != []:
    global event
    event = Event()
    with concurrent.futures.ThreadPoolExecutor(max_workers=2) as executor:
        voice_instruct_future = executor.submit(voice_instruct, event)
        ollama_future = executor.submit(ollama, name=name)
        voice_instruct_future.result()
        ollama_future.result()
    changeme = context.pop(-2)
    changeme['role'] = 'assistant'
    context.append(changeme)
    changeme = context.pop(-2)
    changeme['role'] = 'user'
    context.append(changeme)
    # print(context)