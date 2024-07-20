import json
from os.path import exists
from groq import Groq

if not exists("./aitool/keys.json"):
    with open("./aitool/keys.json", 'w') as f:
        json.dump({"GROQ_API_KEY": "<Put your API key here>"}, f, indent=2)

with open("./aitool/keys.json", 'r') as f:
    keys = json.load(f)

client = Groq(
    api_key=keys["GROQ_API_KEY"],
)


from .post_generator import generate
from .chat import send
