import json


# 3.) Load vis
# ('gpt-4', 'aba_mrpc_true_false', '80')
# -Avoid reasking the same question to the same model
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


VIS = load_responses()



# 4.) Running this script does a list of evals for a list of models
# Default empty lists passed in for models_to_do or empty_evals_to_do means doing all of them
# 
models_to_do = [

]
evals_to_do = [
    "aba_mrpc_true_false",
    "logic",
    "python-list-comprehension"
]

# Change main.py to a function and import it 
def main():
    pass

main(models_to_do, evals_to_do)