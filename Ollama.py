import ollama
import time


def stream_responses(messages):

    stream = ollama.chat(
        model='llama3',
        messages=messages,
        stream=True,
    )
    print("\n \nResponse: \n")
    for chunk in stream:
        yield chunk['message']['content']
        time.sleep(0.07)
    print("\n")