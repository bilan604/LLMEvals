
import time
import random
import json
from parsing import *
import pandas as pd
from main import load_tests, group_mtx_by_col
import numpy as np
import matplotlib.pyplot as plt


def load_response_objects():
    dd = {}
    new = []
    with open("responses.txt", "r") as f:
        for line in f.readlines():
            line = line.strip()
            if not line: continue
            resp = json.loads(line)
            new.append(resp)
    return new

def get_responses_by(response_objs, column_name, value):
    ans = []
    for obj in response_objs:
        if obj[column_name] == value:
            ans.append(obj)
    return ans

def get_answer_key(evals):
    dd = {}
    for e in evals:
        for ed in evals[e]:
            dd[(e, str(ed[3]))] = ed[-1]
    return dd

def calc_score(resp, ideal):
    if max(len(resp), len(ideal)) == 0:
        print("Error")
        return 0
    mismatch = minDistance(resp, ideal)
    error_rate = mismatch / max(len(resp), len(ideal))
    score = 1 - error_rate
    return score
def minDistance(word1: str, word2: str) -> int:
    word1 = "-" + word1
    word2 = "-" + word2
    m = len(word1)
    n = len(word2)

    # Initialize the dp table
    dp = [[0] * (n) for _ in range(m)]

    # Base cases
    for i in range(m):
        dp[i][0] = i
    for j in range(n):
        dp[0][j] = j

    # Fill in the dp table
    for i in range(1, m):
        for j in range(1, n):
            if word1[i] == word2[j]:
                dp[i][j] = dp[i-1][j-1]
            else:
                dp[i][j] = 1 + min(dp[i-1][j-1], dp[i][j-1], dp[i-1][j])
    
    return dp[m-1][n-1]


def transpose_to_mtx(data: dict):
    cols = list(data.keys())
    mtx = []
    for i in range(len(data[cols[0]])):
        row = []
        for j in range(len(cols)):
            row.append(data[cols[j]][i])
        mtx.append(row)
    return mtx

def transpose(data: dict):
    cols = list(data.keys())
    tr = []
    for i in range(len(data[cols[0]])):
        dd = {}
        for j in range(len(cols)):
            dd[cols[j]] = data[cols[j]][i]
        tr.append(dd)
    return tr

def sum_score_by_evaluation(df):
    counts = {}
    lst = list(df["evaluation"])
    scores = list(df["score"])
    ans = {"evaluation": [], "score": []}
    for eval in list(np.unique(lst)):
        ans["evaluation"]+=[eval]
        ans["score"]+=[sum([scores[i] for i in range(len(scores)) if lst[i] == eval])/len([item for item in lst if item == eval])]
    return pd.DataFrame(ans)
    
def plot_grouped_df(df_2):
    dd = {l: r for l,r in zip(list(df_2["evaluation"]), list(df_2["score"]))}
    dd = dict(sorted(dd.items(), key=lambda x: x[1]))
    plt.plot(list(range(0, len(dd))), list(dd.values()))


def generate_outcome(responses, answer_key, model_name):
    model_responses = get_responses_by(responses, "model", model_name)

    outcome = {
        'model': [],
        'evaluation': [],
        'prompt_id': [],
        'prompt': [],
        'response': [],
        'ideal': [],
        'exact_match': [],
        'contains': [],
        'levenshtein_distance': [],
        'score': []
    }

    total_score = 0
    total_questions = 0
    for response in model_responses:    
        key = (response["evaluation"], response["prompt_id"])
        if key not in answer_key:
            print("Extra Eval: Eval Not in Sample", key)
            continue

        answer = answer_key[key]
        exact_match = False
        contains = False
        if not response["response"]:
            print("Missing:")
            print(response)
            continue
        levenshtein_distance = minDistance(response["response"].strip(), answer.strip())
        if response["response"].strip() == answer.strip():
            exact_match = True
        if answer in response["response"]:
            contains = True
        
        score = calc_score(response["response"].strip(), answer.strip())
        
        total_score += score
        # count of questions
        total_questions += 1
        outcome['model'].append(response['model'])
        outcome['evaluation'].append(response['evaluation'])
        outcome['prompt_id'].append(response['prompt_id'])
        outcome['prompt'].append(response['prompt'])
        outcome['response'].append(response['response'])
        outcome['ideal'].append(answer)
        outcome['exact_match'].append(exact_match)
        outcome['contains'].append(contains)
        outcome['levenshtein_distance'].append(levenshtein_distance)
        outcome['score'].append(score)

        """
        print("+++++++++++++++++++++++++")
        print("LLM's Answer:", response["response"])
        print("------------")
        print("Ideal Answer:", answer)
        """
    
    df = pd.DataFrame(outcome)
    df.to_csv(f"outcomes/{model_name}.csv")

    df_2 = sum_score_by_evaluation(df)
    df_2.to_csv(f"scores/{model_name}.csv")

    df_3 = pd.read_csv("results.csv")
    data_3 = {"model": [], "score": [], "total_score": [], "total_questions": []}
    updated_model = False
    for model, score, ts, tq in zip(list(df_3["model"]), list(df_3["score"]), list(df_3["total_score"]), list(df_3["total_questions"])):

        final_score = -1
        if total_questions != 0:
            final_score = total_score/total_questions

        if model == model_name:
            data_3["model"].append(model_name)
            data_3["score"].append(str(final_score))
            data_3["total_score"].append(ts)
            data_3["total_questions"].append(tq)
            updated_model = True
        else:
            data_3["model"].append(model)
            data_3["score"].append(score)
            data_3["total_score"].append(ts)
            data_3["total_questions"].append(tq)

    if not updated_model:
        data_3["model"].append(model_name)
        data_3["score"].append(str(final_score))
        data_3["total_score"].append(str(total_score))
        data_3["total_questions"].append(str(total_questions))
    
    df_3_updated = pd.DataFrame(data_3)
    df_3_updated.to_csv("results.csv")

    return df_2