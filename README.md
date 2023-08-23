# LLMEvals  

## Directory Description:

A sample of eval test suites were created, sampling a maximum of 10 questions from each eval question set. The score for each response is inverse of the fraction of mismatch between the LLM's response and the ideal answer for the eval problem.  

## Notes about using the LLMs in evals  

I was not able to create / reverse engineer an API for some of the language models. The original version of much of the llm prompting code was built towards having a selenium bot interact with websites like www.poe.com and send and recieve messages from LLM's there.

Due to the first solution being blocked by Cloudflare, I determined to sample ten questions from each eval set and create a random sample dataset for the 2100 questions. The code is built so that the pipeline can continue to accumulate sampled questions.








