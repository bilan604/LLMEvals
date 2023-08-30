import json
import time
import numpy as np
import pandas as pd
from load import *
from prompter import handle_prompt_map
from prompter import prompt as do_prompt
from generate_outcome import *

poe_models = []

# Models to Run
models = [
    "gpt-3.5-turbo",
    "gpt-4",
    "llama-1-13b",
    "llama-2-13b",
    "llama-2-70b-chat",
    "vicuna-1-13b",
    "vicuna-1.5-13b",
    "vicuna-1-33b",  
    "claude-2",
    "claude-instant",
    "bard",
    "palm-2",
    "luminous-supreme-control",
    "cohere-chat",
    "falcon-40b",
    "mpt-30b", 
    "inflection-1"  
]

# Models that have been run for sample
completed_models = [
    'gpt-3.5-turbo'
]

models_to_implement = [
    "falcon-40b",  # hugging face: 
    "vicuna-1.5-13b",  # https://huggingface.co/lmsys/vicuna-13b-v1.5
    "vicuna-1-33b",  # https://huggingface.co/TheBloke/Vicuna-33B-1-3-SuperHOT-8K-fp16
    "falcon-40b",  # https://huggingface.co/tiiuae/falcon-40b
    "mpt-30b",  # https://huggingface.co/mosaicml/mpt-30b
    "inflection-1" # not on hugging face
]

############################
# 3.) Load vis
# Avoids reasking the same question to the same model
# Like: ('gpt-4', 'aba_mrpc_true_false', '80')
# NOTE: load_responses doesn't return the entire response data, just the unique identifier
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

# 3.)
VIS = load_responses()


############################
# 4.) Load the data for the tests
def load_tests(filepath):
    df = pd.read_csv(filepath)
    print(df)
    mtx = np.array(df)
    return mtx

# 4.)
tests = load_tests("prompts.csv")




# function for running tests
def run_test(model, evaluation, prompt, test_idx):
    # evaluation is the name of the folder
    # prompt is the string prompt
    # test_idx is index of the prompt from evaluation folder
    print(f"run_test(): Running prompt number {test_idx} for eval {evaluation}")
    try:
        response = do_prompt(model, prompt)
        print(f"run_test():\n{response=}\n")
        save_response(model, evaluation, str(test_idx), prompt, response)
        return
    except Exception as e:
        print("Error:", e)
        print("Condition:", isinstance(e, openai.error.RateLimitError))
        if isinstance(e, openai.error.RateLimitError):
            print("Sleeping for 60 seconds")
            time.sleep(60)
            response = do_prompt(model, prompt)
            print(f"run_test():{response=}\n")
            save_response(model, evaluation, str(test_idx), prompt, response)
            
        return

def get_relevance():
    rel = {}
    with open("relevance.txt", "r") as f:
        for line in f.readlines():
            if not ("," in line): continue
            k,v = line.strip().split(",")
            rel[k.strip()] = v.strip()
    return rel

def main(models_todo: list[str], evals_todo: list[str], VIS):
    """
    Need to for each model to do, and each eval to do, check vis and do the eval.
    """
    env = get_env()
    OPENAI_API_KEY = env["OPENAI_API_KEY"]
    openai.api_key = OPENAI_API_KEY

    evals = group_mtx_by_col(tests, 1)
    relevance = get_relevance()
    if not models_todo:
        global models
        models_current_eval = models
    else:
        models_current_eval = models_todo
    
    if not evals_todo:
        pass
    else:
        evals = {k: evals[k] for k in evals_todo}


    for model in models_current_eval:
        for eval in evals:
            for i in range(len(evals[eval])):
                eval_data = evals[eval][i]

                vis_key = (model, eval, str(eval_data[3]))
                if vis_key in VIS:
                    print("skipping vis:", vis_key)
                    continue

                if eval not in relevance:
                    print(f"relevance for {eval} not set")
                    continue

                ########
                # for now, conduct the high relevance evals
                # due to api costs
                if int(relevance[eval]) < 7:
                    print(f"relevance for {eval} not set")
                    continue
                
                run_test(model, eval, eval_data[2], eval_data[3])
            

if __name__ == "__main__":
    # 4.) Running this script does a list of evals for a list of models
    # Default empty lists passed in for models_to_do or empty_evals_to_do means doing all of them
    """
    models_to_do = [
        "llama-1-13b",
        "llama-2-13b",
        "llama-2-70b-chat",
        "vicuna-1-13b",
        "vicuna-1.5-13b",
        "vicuna-1-33b",  
        "claude-2",
        "claude-instant",
        "luminous-supreme-control",
        "cohere-chat",
        "falcon-40b",
        "mpt-30b", 
        "inflection-1" 
    ]

    evals_to_do = [
        '2d_movement'
    ]
    
    VIS = load_responses()
    main(models_to_do, evals_to_do, VIS)
    """
    ##########
    # 5.) Generating outcomes
    # get tests to get evals dict to get answer key dict
    tests = load_tests("prompts.csv")
    evals = group_mtx_by_col(tests, 1)

    answer_key = get_answer_key(evals)
    responses = load_response_objects()
    model_tables = {}
    for model in handle_prompt_map:
        print("Generating outcome for")
        print("model:", model)
        model_tables[model] = generate_outcome(responses, answer_key, model)
    
    update_readme(model_tables)

    # 6.) To increase the sample in the future, run the sample evals script
    # and concatenate it with the existing prompts