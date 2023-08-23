import os
#os.environ["CUDA_VISIBLE_DEVICES"]="1,2" # if you need to specify GPUs
import time
from transformers import AutoTokenizer, AutoModelForCausalLM, TextStreamer
import transformers
import torch

model_id = "tiiuae/falcon-40b-instruct"

tokenizer = AutoTokenizer.from_pretrained(model_id)
streamer = TextStreamer(tokenizer)

model = AutoModelForCausalLM.from_pretrained(
    model_id,
    # --- Choosing between 4, 8, and 16 bit --- #
    # 8bit: ~50GB GPU memory, fastest
    # 4bit: ~25GB GPU memory, slowest 
    # 16bit: ~100GB GPU memory, slow
    load_in_8bit=True, # torch_dtype=torch.bfloat16 or load_in_4bit=True
    trust_remote_code=True,
    device_map="auto",
)

pipeline = transformers.pipeline(
    "text-generation",
    model=model,
    tokenizer=tokenizer,
)
print(f"{pipeline=}\n")