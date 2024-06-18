import Transcription
import Ollama
import time
import os
import concurrent.futures


context = []
def add_context(role, content):
    context.append({'role': role, 'content': content})

def voice_instruct():
            voice_instruct = Transcription.transcribe_return()
            add_context('user', voice_instruct)
            print("\n")

def ollama():
    init_context = context.copy()
    gen = Ollama.stream_responses(init_context)
    response = ""
    while True:
        try:
            if context == init_context:
                token = next(gen)
                print(token, end="", flush=True)
                # Add token to response
                response += token
                # OPTIONAL tts
                # if token.isalpha():
                #     os.system(f'say {token}')
            else:
                #  print("CONTEXT CHANGED")
                 user_text = context.pop(-2)
                 context.append(user_text)
                 break
        except StopIteration:
            return response
    add_context('assistant', response)
voice_instruct()
while True:
    with concurrent.futures.ThreadPoolExecutor(max_workers=2) as executor:
        voice_instruct_future = executor.submit(voice_instruct)
        ollama_future = executor.submit(ollama)
        voice_instruct_future.result()
        response = ollama_future.result()
    # print(context)