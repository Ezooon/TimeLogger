# LLaMa Get started Guide

import json
from llamaapi import LlamaAPI

# Initialize the SDK
llama = LlamaAPI("LL-FCfAPJo8sUykdWs0f3mdBAQ3kfUYlq8zpkqMzBg0zCTQ8sujB6lB6EWhfcp1pnB1")

# Build the API request
api_request_json = {
    "messages": [
        {"role": "user", "content": "What is the weather like in Boston?"},
    ],
    "functions": [
        {
            "name": "get_current_weather",
            "description": "Get the current weather in a given location",
            "parameters": {
                "type": "object",
                "properties": {
                    "location": {
                        "type": "string",
                        "description": "The city and state, e.g. San Francisco, CA",
                    },
                    "days": {
                        "type": "number",
                        "description": "for how many days ahead you wants the forecast",
                    },
                    "unit": {"type": "string", "enum": ["celsius", "fahrenheit"]},
                },
            },
            "required": ["location", "days"],
        }
    ],
    "stream": False,
    "function_call": "get_current_weather",
}

# Execute the Request
response = llama.run(api_request_json)
print(json.dumps(response.json(), indent=2))
# { # Other parameters that you can pass in the request json are:
#   ...
#   "max_token" = 500,
#   "temperature"= 0.1,
#   "top_p"= 1.0,
#   "frequency_penalty"=1.0
#   ...
# }
