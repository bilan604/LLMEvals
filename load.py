import openai
import os
import json

def get_env(file_path=".env"):
    env = {}
    with open(file_path, "r") as f:
        for line in f.readlines():
            line = line.strip()
            if line:
                lst = line.split("=")
                env[lst[0].strip()] = lst[1].strip()
    return env

def load_env():
    env = get_env()
    OPENAI_API_KEY = env["OPENAI_API_KEY"]
    openai.api_key = OPENAI_API_KEY
    return

def load_evaluations(n=10):
    evaluations = {}

    cwd = "C:/Users/Bill/projects/llm-evals/evals/data"
    os.chdir(cwd)

    folders = []
    for folder in os.listdir():
        folders.append(folder)

    for folder in folders:
        #################
        if len(evaluations) == n:
            break

        path = "C:/Users/Bill/projects/llm-evals/evals/data/" + folder
        os.chdir(path)
        for file in os.listdir():
            if not os.path.isfile(file): continue
            try:
                with open(file, "r") as f:
                    lines = f.readlines()
                    lines = [json.loads(line) for line in lines]
                    evaluations[folder] = lines
                    break
            except:
                print("samples.jsonl missing for", folder)

    os.chdir(cwd)

    return evaluations