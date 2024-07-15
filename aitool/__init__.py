import json

from groq import Groq

with open("./aitool/keys.json", 'r') as f:
    keys = json.load(f)

client = Groq(
    api_key=keys["GROQ_API_KEY"],
)


from .post_generator import generate
from .chat import send
