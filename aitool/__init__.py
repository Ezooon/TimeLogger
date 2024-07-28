import json
from os.path import exists
from groq import Groq
from utils import resource_path

keypa = resource_path("./aitool/keys.json")
if not exists(keypa):
    with open(keypa, 'w') as f:
        json.dump({"GROQ_API_KEY": "<Put your API key here>"}, f, indent=2)

with open(keypa, 'r') as f:
    keys = json.load(f)

client = Groq(
    api_key=keys["GROQ_API_KEY"],
)


from .post_generator import generate
from .chat import send
