# LLMEvals Repository


# LLMEvals  

Usage:  
1. make a .env file containing the contents of the .env.sample file. The .env file is not ommited in this repository because it is private
2. Run ```python main.py``` in git bash. You may get errors for installing packages, which can be installed with ```pip install name-of-package```

## Directory Description:
sample_evals.py: generates a sample of the evals of approximately 2100 evals problems of the 450,000 problems present.

main.py:
-checks which evals still need to be done, skipping saved evals  
-updates the saved data for how the models performed on the evals  
-updates the readme template  



## Model Scores:

<table>
<tr>
<td>0</td>
<td>gpt-3.5-turbo</td>
<td>0.332697211788481</td>
<td>1971.80818415302</td>
<td>2156</td>
</tr>
<tr>
<td>1</td>
<td>gpt-4</td>
<td>0.3975545385630731</td>
<td>72.90714285714286</td>
<td>88</td>
</tr>
<tr>
<td>2</td>
<td>llama-1-13b</td>
<td>0.0065288356909684</td>
<td>1.0</td>
<td>1</td>
</tr>
<tr>
<td>3</td>
<td>llama-2-13b</td>
<td>-1.0</td>
<td>0.0</td>
<td>0</td>
</tr>
<tr>
<td>4</td>
<td>llama-2-70b-chat</td>
<td>0.1314704930696055</td>
<td>2087.140476190476</td>
<td>2142</td>
</tr>
<tr>
<td>5</td>
<td>vicuna-1-13b</td>
<td>-1.0</td>
<td>0.0</td>
<td>0</td>
</tr>
<tr>
<td>6</td>
<td>vicuna-1.5-13b</td>
<td>-1.0</td>
<td>0.0</td>
<td>0</td>
</tr>
<tr>
<td>7</td>
<td>vicuna-1-33b</td>
<td>-1.0</td>
<td>0.0</td>
<td>0</td>
</tr>
<tr>
<td>8</td>
<td>claude-2</td>
<td>-1.0</td>
<td>0.0</td>
<td>0</td>
</tr>
<tr>
<td>9</td>
<td>claude-instant</td>
<td>-1.0</td>
<td>0.0</td>
<td>0</td>
</tr>
<tr>
<td>10</td>
<td>bard</td>
<td>-1.0</td>
<td>0.0</td>
<td>0</td>
</tr>
<tr>
<td>11</td>
<td>luminous-supreme-control</td>
<td>-1.0</td>
<td>0.0</td>
<td>0</td>
</tr>
<tr>
<td>12</td>
<td>cohere-chat</td>
<td>-1.0</td>
<td>0.0</td>
<td>0</td>
</tr>
<tr>
<td>13</td>
<td>falcon-40b</td>
<td>-1.0</td>
<td>0.0</td>
<td>0</td>
</tr>
<tr>
<td>14</td>
<td>mpt-30b</td>
<td>-1.0</td>
<td>0.0</td>
<td>0</td>
</tr>
<tr>
<td>15</td>
<td>inflection-1</td>
<td>-1.0</td>
<td>0.0</td>
<td>0</td>
</tr>
<tr>
<td>16</td>
<td>palm-2</td>
<td>-1.0</td>
<td>0.0</td>
<td>0</td>
</tr>
</table>




## Model Scores by Model for each Eval:

{results_tables_by_model_by_eval}



## Notes about using the LLMs in evals  



I was not able to create / reverse engineer an API for some of the language models. The original version of much of the llm prompting code was built towards having a selenium bot interact with websites like www.poe.com and send and recieve messages from LLM's there.



Due to the first solution being blocked by Cloudflare, I determined to sample ten questions from each eval set and create a random sample dataset for the 2100 questions. The code is built so that the pipeline can continue to accumulate sampled questions.
