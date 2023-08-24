# LLMEvals Repository

# LLMEvals  

## Directory Description:

sample_evals.py: generates a sample of the evals of approximately 2100 evals problems of the 450,000 problems present.

main.py:
-checks which evals still need to be done, skipping saved evals
-updates the saved data for how the models performed on the evals
-updates the readme template

## Model Scores:
{results_table}

## Model Scores by Model for each Eval:
{results_tables_by_model_by_eval}

## Notes about using the LLMs in evals  

I was not able to create / reverse engineer an API for some of the language models. The original version of much of the llm prompting code was built towards having a selenium bot interact with websites like www.poe.com and send and recieve messages from LLM's there.

Due to the first solution being blocked by Cloudflare, I determined to sample ten questions from each eval set and create a random sample dataset for the 2100 questions. The code is built so that the pipeline can continue to accumulate sampled questions.
