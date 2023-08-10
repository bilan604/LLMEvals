import time
import pandas as pd

from load import *

from language_models import Prompter
load_env()


evaluations = load_evaluations()
print(list(evaluations.keys()))

evaluations_todo = ['2d_movement']

prompter = Prompter()



def test_model(prompter, model, tests):
    idx = 0
    verdicts = []
    while idx < len(tests):
        test = tests[idx]
        # openai message format
        query = test['input']
        print("query:",query)

        response = None
        try:
            response = prompter.prompt(model, query)
            print(response)
        except Exception as e:
            print("Error:", e)
            print("Condition:", isinstance(e, openai.error.RateLimitError))
            if isinstance(e, openai.error.RateLimitError):
                print("Sleeping for 60 seconds")
                time.sleep(60)
            else:
                return verdicts

        if response:
            if response == test['ideal']:
                verdicts.append(True)
            else:
                verdicts.append(False)
        
        idx += 1
    
    return verdicts


# Boolean Tests
print(list(prompter.model_map.keys()))

models = ['gpt-4', 'bard']
data = {"Model": [], "Test": [], "Accuracy": []}
for model in models:
    for evaluation in evaluations_todo:
        tests = evaluations[evaluation]
        verdicts = test_model(prompter, model, tests)
        if not verdicts:
            print("No verdicts for", model, evaluation)
            continue

        accuracy = len([v for v in verdicts if v]) / len(verdicts)

        data["Model"].append(model)
        data["Test"].append(evaluation)
        data["Accuracy"].append(accuracy)


if len(data["Model"]) > 0:

    print(data)
    import os
    os.chdir("C:/Users/Bill/projects/llm-evals")
    df = pd.DataFrame(data)
    df.to_csv("results.csv")

