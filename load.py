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


def save_response(model, evaluation, prompt_idx,  prompt, response):
    obj = {
        "model": model,
        "evaluation": evaluation,  # the problem set
        "prompt_id": prompt_idx,
        "prompt": prompt ,
        "response": response
    }
    with open("responses.txt", "a") as f:
        f.write(json.dumps(obj)+"\n")
    return


def load_responses():
    """
    Loads Vis
    """
    dd = {}
    with open("responses.txt", "r") as f:
        for line in f.readlines():
            line = line.strip()
            if not line: continue
            resp = json.loads(line)
            k = (resp["model"], resp["evaluation"], resp["prompt_id"])
            dd[k] = True
    return dd

def group_mtx_by_col(mtx, col):
    dd = {}
    for i in range(len(mtx)):
        if mtx[i][col] not in dd:
            dd[mtx[i][col]] = []
        dd[mtx[i][col]].append(mtx[i])
    return dd