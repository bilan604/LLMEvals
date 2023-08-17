import openai
from bardapi import Bard


bard = None  #Bard()


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

def prompt_bard(prompt):
    resp = bard.objects['bard'].get_answer(prompt)
    response = resp["content"]
    return response

def prompt_vicuna_1_5_13b(prompt):
    pass

def prompt_llama_1_13b(prompt):
    pass

def prompt_vicuna_1_13b(prompt):
    pass

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

handle_prompt_map = {
    "gpt-3.5-turbo": prompt_gpt_3_5,
    "gpt-4": prompt_gpt_4,
    "bard": prompt_bard,
    "vicuna-1.5-13b": prompt_vicuna_1_5_13b,
    "llama-1-13b": prompt_llama_1_13b,
    "vicuna-1-13b": prompt_vicuna_1_13b,
    "vicuna-1-33b": prompt_vicuna_1_33b,
    "luminous-supreme-control": prompt_luminous_supreme_control,
    "cohere-chat": prompt_cohere_chat,
    "falcon-40b": prompt_falcon_40b,
    "mpt-30b": prompt_mpt_30b,
    "inflection-1": prompt_inflection_1
}

def prompt(model, prompt):
    resp = handle_prompt_map[model](prompt)
    return resp