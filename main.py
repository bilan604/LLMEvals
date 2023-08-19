import json
import time
import numpy as np
import pandas as pd
from load import *
from prompt_2 import prompt as do_prompt


# Globals Variables
poe_models = [ 
    "Claude-2-100k",
    "Claude-instant",
    "GPT-4-32k",
    "Google-PaLM",
    "Llama-2-70b",
    "Llama-2-13b",
    "Llama-2-7b"
]

models = [
        'gpt-4',
        'gpt-3.5-turbo',
        'bard',
        # Poe Models
        "Claude-2-100k",
        "Claude-instant",
        "GPT-4-32k",
        "Google-PaLM",
        "Llama-2-70b",
        "Llama-2-13b",
        "Llama-2-7b"
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
    print("AT RUN TEST")
    
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
            response = prompt(model, prompt)
            print(f"run_test():{response=}\n")
            save_response(model, evaluation, str(test_idx), prompt, response)
            
        return


def main(models_todo: list[str], evals_todo: list[str], VIS):
    """
    Need to for each model to do, and each eval to do, check vis and do the eval.
    """
    env = get_env()
    OPENAI_API_KEY = env["OPENAI_API_KEY"]
    openai.api_key = OPENAI_API_KEY

    evals = group_mtx_by_col(tests, 1)
    
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
            # do the tests
            for i in range(len(evals[eval])):
                ########################################################
                # get the grouped data
                eval_data = evals[eval][i]
                run_test(model, eval, eval_data[2], eval_data[3])
            
        
#2452
if __name__ == "__main__":
    # 4.) Running this script does a list of evals for a list of models
    # Default empty lists passed in for models_to_do or empty_evals_to_do means doing all of them
    models_to_do = [
        'bard'
    ]
    evals_to_do = [
    ]
    VIS = load_responses()
    main(models_to_do, evals_to_do, VIS)

