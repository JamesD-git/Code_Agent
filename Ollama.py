import ollama
import time


def stream_responses(messages):
    print("\n \nResponse: \n")
    stream = ollama.chat(
        model='llama3',
        messages=messages,
        stream=True,
    )

    for chunk in stream:
        yield chunk['message']['content']
    print("\n")