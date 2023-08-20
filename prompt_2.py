import openai
import replicate
from bardapi import Bard
from load import get_env


env = get_env()
token = env["BARD_API_KEY"].strip()
bard = None
try:
    bard = Bard(token=token)
except Exception as e:
    print("Bard Error:", e)


client = replicate.Client(api_token='r8_9S4jrLb3J7Y6lnlole7ww2L7ezeaMU62X8vMT')


def prompt_gpt_3_5(input_content: str):
    input=[{"role": "system", "content": "You are a helpful assistant."},{"role": "user", "content": input_content}]
    # hyperparameters are set literal
    response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=input,
            temperature=0.0,
            max_tokens=1000,
            frequency_penalty=0.0
        ).choices[0].message.content.strip()
    return response

def prompt_gpt_4(input_content: str):
    input=[{"role": "system", "content": "You are a helpful assistant."},{"role": "user", "content": input_content}]
    # hyperparameters are set literal
    response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=input,
            temperature=0.0,
            max_tokens=1000,
            frequency_penalty=0.0
        ).choices[0].message.content.strip()
    return response

# Note: This is not 1.5?
def get_vicuna_13b_output(client, prompt: str):
    output = client.run(
        "replicate/vicuna-13b:6282abe6a492de4145d7bb601023762212f9ddbbe78278bd6771c8b3b2f2a13b",
        input={"prompt": prompt}
    )

    response_chunks = []
    for item in output:
        # https://replicate.com/replicate/vicuna-13b/versions/6282abe6a492de4145d7bb601023762212f9ddbbe78278bd6771c8b3b2f2a13b/api#output-schema
        response_chunks.append(item)

    response = " ".join(response_chunks)
    response = response.replace("  ", " ").strip()
    print("----------------> response:")
    print(response)
    return response

def get_llama_13b_lora_output(client, prompt: str):
    output = client.run(
        "replicate/llama-13b-lora:4baede730d6bc13396e6dec0df5172bff658c014da9552bc17decfd6453d368c",
        input={"prompt": prompt}
    )

    response_chunks = []
    for item in output:
        # https://replicate.com/replicate/vicuna-13b/versions/6282abe6a492de4145d7bb601023762212f9ddbbe78278bd6771c8b3b2f2a13b/api#output-schema
        response_chunks.append(item)

    response = " ".join(response_chunks)
    response = response.replace("  ", " ").strip()
    print("----------------> response:")
    print(response)
    return response


def get_llama_2_7b_output(client, prompt: str):
    output = client.run(
        "replicate/llama-2-7b:acdbe5a4987a29261ba7d7d4195ad4fa6b62ce27b034f989fcb9ab0421408a7c",
        input={"prompt": prompt}
    )

    response_chunks = []
    for item in output:
        response_chunks.append(item)

    response = " ".join(response_chunks)
    response = response.replace("  ", " ").strip()
    print("----------------> response:")
    print(response)
    return response


def get_llama_2_70b_chat_output(client, prompt: str):
    output = client.run(
        "replicate/llama-2-70b-chat:58d078176e02c219e11eb4da5a02a7830a283b14cf8f94537af893ccff5ee781",
        input={"prompt": prompt}
    )

    response_chunks = []
    for item in output:
        response_chunks.append(item)

    response = " ".join(response_chunks)
    response = response.replace("  ", " ").strip()
    print("----------------> response:")
    print(response)
    return response

# Note: This is chat
def get_llama_2_13b_chat_output(client, prompt: str):
    output = client.run(
        "a16z-infra//llama-2-13b-chat:2a7f981751ec7fdf87b5b91ad4db53683a98082e9ff7bfd12c8cd5ea85980a52",
        input={"prompt": prompt}
    )

    response_chunks = []
    for item in output:
        response_chunks.append(item)

    response = " ".join(response_chunks)
    response = response.replace("  ", " ").strip()
    print("----------------> response:")
    print(response)
    return response

#######
def prompt_bard(prompt):
    resp = bard.objects['bard'].get_answer(prompt)
    response = resp["content"]
    return response

def prompt_vicuna_1_5_13b(prompt):
    # Note: 1.5
    global client
    return get_vicuna_13b_output(client, prompt)

def prompt_llama_1_13b(prompt):
    global client
    return get_llama_13b_lora_output(client, prompt)

def prompt_vicuna_1_13b(prompt):
    global client
    return get_vicuna_13b_output(client, prompt)

def prompt_vicuna_1_33b(prompt):
    pass

def prompt_luminous_supreme_control(prompt):
    pass

def prompt_cohere_chat(prompt):
    pass

def prompt_falcon_40b(prompt):
    pass

def prompt_mpt_30b(prompt):
    pass

def prompt_inflection_1(prompt):
    pass

def prompt_llama_2_13b(prompt):
    # note: chat
    global client
    return get_llama_2_13b_chat_output(client, prompt)

def prompt_llama_2_70b_chat(prompt):
    global client
    return get_llama_2_70b_chat_output(client, prompt)

def prompt_claude_2(prompt):
    pass

def prompt_claude_instant(prompt):
    pass

def prompt_palm_2(prompt):
    pass

handle_prompt_map = {
    "gpt-3.5-turbo": prompt_gpt_3_5,  #
    "gpt-4": prompt_gpt_4,  #

    "llama-1-13b": prompt_llama_1_13b,  #
    "llama-2-13b": prompt_llama_2_13b,  #
    "llama-2-70b-chat": prompt_llama_2_70b_chat,
    "vicuna-1-13b": prompt_vicuna_1_13b, #
    "vicuna-1.5-13b": prompt_vicuna_1_5_13b,  #
    "vicuna-1-33b": prompt_vicuna_1_33b,  #

    "claude-2": prompt_claude_2, 
    "claude-instant": prompt_claude_instant,
    "bard": prompt_bard,

    "luminous-supreme-control": prompt_luminous_supreme_control,
    "cohere-chat": prompt_cohere_chat,
    "falcon-40b": prompt_falcon_40b,
    "mpt-30b": prompt_mpt_30b,
    "inflection-1": prompt_inflection_1,
    "palm-2": prompt_palm_2  # Fill in the actual function name
}

def prompt(model, prompt):
    resp = handle_prompt_map[model](prompt)
    return resp

