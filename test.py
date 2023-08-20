import replicate

# Notes on vicuna_13 and llama-2-13b

# Note: This is not 1.5?
def get_vicuna_13b_output(client, prompt: str):
    output = client.run(
        "replicate/vicuna-13b:6282abe6a492de4145d7bb601023762212f9ddbbe78278bd6771c8b3b2f2a13b",
        input={"prompt": prompt}
    )

    response_chunks = []
    for item in output:
        # https://replicate.com/replicate/vicuna-13b/versions/6282abe6a492de4145d7bb601023762212f9ddbbe78278bd6771c8b3b2f2a13b/api#output-schema
        response_chunks.append(item)

    response = " ".join(response_chunks)
    response = response.replace("  ", " ").strip()
    print("----------------> response:")
    print(response)
    return response

def get_llama_13b_lora_output(client, prompt: str):
    output = client.run(
        "replicate/llama-13b-lora:4baede730d6bc13396e6dec0df5172bff658c014da9552bc17decfd6453d368c",
        input={"prompt": prompt}
    )

    response_chunks = []
    for item in output:
        # https://replicate.com/replicate/vicuna-13b/versions/6282abe6a492de4145d7bb601023762212f9ddbbe78278bd6771c8b3b2f2a13b/api#output-schema
        response_chunks.append(item)

    response = " ".join(response_chunks)
    response = response.replace("  ", " ").strip()
    print("----------------> response:")
    print(response)
    return response


def get_llama_2_7b_output(client, prompt: str):
    output = client.run(
        "replicate/llama-2-7b:acdbe5a4987a29261ba7d7d4195ad4fa6b62ce27b034f989fcb9ab0421408a7c",
        input={"prompt": prompt}
    )

    response_chunks = []
    for item in output:
        response_chunks.append(item)

    response = " ".join(response_chunks)
    response = response.replace("  ", " ").strip()
    print("----------------> response:")
    print(response)
    return response


def get_llama_2_7b_output(client, prompt: str):
    output = client.run(
        "replicate/llama-2-7b:acdbe5a4987a29261ba7d7d4195ad4fa6b62ce27b034f989fcb9ab0421408a7c",
        input={"prompt": prompt}
    )

    response_chunks = []
    for item in output:
        response_chunks.append(item)

    response = " ".join(response_chunks)
    response = response.replace("  ", " ").strip()
    print("----------------> response:")
    print(response)
    return response


def get_llama_2_70b_chat_output(client, prompt: str):
    output = client.run(
        "replicate/llama-2-70b-chat:58d078176e02c219e11eb4da5a02a7830a283b14cf8f94537af893ccff5ee781",
        input={"prompt": prompt}
    )

    response_chunks = []
    for item in output:
        response_chunks.append(item)

    response = " ".join(response_chunks)
    response = response.replace("  ", " ").strip()
    print("----------------> response:")
    print(response)
    return response

# Note: This is chat
def get_llama_2_13b_chat_output(client, prompt: str):
    output = client.run(
        "a16z-infra//llama-2-13b-chat:2a7f981751ec7fdf87b5b91ad4db53683a98082e9ff7bfd12c8cd5ea85980a52",
        input={"prompt": prompt}
    )

    response_chunks = []
    for item in output:
        response_chunks.append(item)

    response = " ".join(response_chunks)
    response = response.replace("  ", " ").strip()
    print("----------------> response:")
    print(response)
    return response


