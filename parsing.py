"""
Code for parsing html for automating online llm responses
"""
import re
import pandas as pd
import numpy as np

def get_opening_tag(s):
    return s[:s.find(">")+1]

def get_element_type(element):
    return element[1:element.find(" ")]

def parse_input(input):
    """
    Converts an OpenAI registry evaluation input to a generalized llm prompt
    In case theres more than just a system prompt
    """
    system_cont = ""
    user_cont = ""
    for pe in input:
        if pe["role"] == "system":
            system_cont = pe["content"]
        elif pe["role"] == "user":
            user_cont = pe["content"]
    
    prompt = \
    """\
{system_cont}

{user_cont}"""

    prompt = re.sub("{system_cont}", system_cont, prompt)
    prompt = re.sub("{user_cont}", user_cont, prompt)        
    return prompt

def handle_aleph_alpha_response(s):
    s = s.strip()
    lst = s.split("\n")
    lst = [li.strip() for li in lst if li.strip()]
    dd = {}
    for item in lst:
        if item not in dd:
            dd[item] = 0
        dd[item] += 1

    idx = 1
    for i in range(1,len(lst)):
        if dd[lst[i]] > 1:
            idx = i
            break
    lst = lst[:idx]
    return "\n".join(lst[:idx])

def make_table(data):
    df = pd.DataFrame(data)
    table = "<table>\n"    
    mtx = np.asarray(df)

    for i in range(len(mtx)):
        row = "<tr>\n"
        for j in range(len(mtx[i])):
            row += "<td>" + str(mtx[i,j]) + "</td>\n"
        row += "</tr>\n"
        table += row
    table += "</table>\n"
    return table

def make_table_from_df(df):
    return make_table(df.to_dict())

def update_readme(model_dataframes):
    df_results = pd.read_csv("results.csv")
    table = make_table(df_results)

    lines = []
    with open("readme_template.txt", "r") as f:
        lines = f.readlines()
    readme = "\n".join(lines)

    readme = re.sub("{results_table}", table, readme)

    results_tables_by_model_by_eval = ""
    for model in model_dataframes:
        model_table = make_table_from_df(model_dataframes[model])
        content = f"""## {model}:

{model_table}

"""
        results_tables_by_model_by_eval += content


    readme = re.sub("{results_tables_by_model_by_eval}", results_tables_by_model_by_eval, readme)

    print("---------")
    print(readme)
    print("<--", readme)
    with open("README.md", "w+") as f:
        f.write(readme)
