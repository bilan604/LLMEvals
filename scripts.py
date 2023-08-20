
def make_functions():
    import re

    lst = ["replicate/llama-2-7b:acdbe5a4987a29261ba7d7d4195ad4fa6b62ce27b034f989fcb9ab0421408a7c",
    "replicate/vicuna-13b:6282abe6a492de4145d7bb601023762212f9ddbbe78278bd6771c8b3b2f2a13b",
    "replicate/llama-2-7b:acdbe5a4987a29261ba7d7d4195ad4fa6b62ce27b034f989fcb9ab0421408a7c",
    "replicate/llama-2-70b-chat:58d078176e02c219e11eb4da5a02a7830a283b14cf8f94537af893ccff5ee781",
    "a16z-infra/llama-2-13b-chat:2a7f981751ec7fdf87b5b91ad4db53683a98082e9ff7bfd12c8cd5ea85980a52"]

    for item in lst:
        lllst = item.split("/")

        item = lllst[1]
        llst = item.split(":")
        func_name = re.sub("-","_",llst[0])
        s = \
        """
    def get_{func_name}_output(client, prompt: str):
        output = client.run(
            \"{lllst}/{item}\",
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
        """
        s = s.replace("{func_name}", func_name)
        s = s.replace("{item}", item)
        s = s.replace("{lllst}", lllst[0])
        print(s)