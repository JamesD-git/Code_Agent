import ollama
import time


def stream_responses(messages):
    print("\n \n Response: \n")
    stream = ollama.chat(
        model='llama3',
        messages=messages,
        stream=True,
    )

    for chunk in stream:
        print(chunk['message']['content'], end='', flush=True)
        time.sleep(0.1)
    print("\n")