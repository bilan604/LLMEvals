import os
import re
import json
import time
import random
import pandas as pd
from parsing import parse_input


def load_evals(cwd = "C:/Users/bill/github/LLMEvals"):
    os.chdir(cwd)

    data_dir = cwd + "/evals/data"
    os.chdir(data_dir)

    folders = []
    for folder in os.listdir():    
        folders.append(folder)

    evaluations = {}    
    for folder in folders:
        lines = []
        try:
            with open(folder + "/samples.jsonl", "r") as f:
                for line in f.readlines():
                    line = line.strip()
                    if not line:
                        continue
                    lines.append(json.loads(line))

            # Need the name of the folder
            evaluations[folder] = lines
        except Exception as e:
            pass
    
    os.chdir(cwd)
    return evaluations


# 1.) Load the evals into a standardized prompt so that different LLM's can have
# the same format of input.
evaluations = load_evals("C:/Users/bill/github/LLMEvals")

def normalize_evals(evaluations):
    evals = {}
    for eval in evaluations:    
        prompts = []
        ideals = []
        for test in evaluations[eval]:
            if "ideal" in test:
                
                try:
                    prompt = parse_input(test["input"])
                    prompts.append(prompt)
                    ideals.append(test['ideal'])
                except:
                    pass
        evals[eval] = {"prompts": prompts, "ideals": ideals}
    return evals

evaluations = normalize_evals(evaluations)        
print("Normalized:", len(evaluations))


def sample(population_size: int, n: int):    
    # Gives a list of indexes for a sample of size n
    if population_size < n:
        return [i for i in range(population_size)]
    if population_size == n:
        return [i for i in range(population_size)]
    
    idxs = set({})
    while len(idxs) < n:
        num = random.randint(0, population_size)
        if num not in idxs:
            idxs.add(num)
    idxs = sorted(list(idxs))
    return idxs

def get_prompts_by_evaluations(evaluations):
    # prompt_id is an index for the prompt
    data = {"evaluation": [], "prompt": [], "prompt_id": [], "ideals": []}
    for eval, prompts_ideals in evaluations.items():
        prompts = prompts_ideals["prompts"]
        ideals = prompts_ideals["ideals"]
        ##########################################
        # The maximum number of questions to use per eval is being set here
        idxs = sample(len(prompts)-1, 10)
        for i in idxs:
            data["evaluation"].append(eval)
            data["prompt"].append(prompts[i])
            data["prompt_id"].append(str(i))
            data["ideals"].append(ideals[i])

    return data

# 2.) Load the prompts and save them to a dataframe
# -easier load and save
# -since the total number is large, and evals differ in relevance from
# eval to eval, all evals are taken into consideration
# and a maximum of 10 is sampled
# which is a scalable solution.
data = get_prompts_by_evaluations(evaluations)
df = pd.DataFrame(data)
print(df)
df.to_csv("prompts.csv")

