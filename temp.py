import json
from parsing import parse_input

def load_responses():
    """
    Loads Vis
    """
    dd = {}
    new = []
    with open("responses.txt", "r") as f:
        for line in f.readlines():
            line = line.strip()
            if not line: continue
            resp = json.loads(line)
            resp["prompt"] = parse_input(resp["prompt"])
            new.append(resp)
    
    with open("responses.txt", "a") as f:
        for n in new:
            f.write(json.dumps(n)+"\n")






load_responses()