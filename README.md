# LLMEvals  

## Directory Description:

language_models.py contains a wrapper that will incorporate various llms.
responses.json is used to store the responses so that all information is not discarded during an eval if the api connection breaks

## Notes about using the LLMs in evals  

1. OpenAI has a token limit which resets every 60 seconds, so pausing during the testing is hard coded in the prompter

2. Bard will stop responding after a while, and the browser cookies have to be cleared.










