import json
from database import Entry

entries = Entry.table.get_items()

from groq import Groq

with open("./aitool/keys.json", 'r') as f:
    keys = json.load(f)

client = Groq(
    api_key=keys["GROQ_API_KEY"],
)

schema = {
    "content": "the tweet's body",
    "suggested_images": [
        "a description of a relevant image the user can attach to boost engagement",
        "..."
    ],
}


def generate(entries,
             num="3",  # the number of posts.
             area="dev logs",  # Is it related to a specific industry or niche?
             tone="humorous",
             # Do you have any specific tone or style (e.g. formal, informal, humorous, inspirational)?
             theme="update",
             # Are there any specific themes or topics you'd like to cover (e.g. news, update, promotion, etc.)?
             keywords=[],  # Are there any specific keywords you'd like to include?
             hashtags=[],  # Are there any specific hashtags you'd like to include?
             callback=print,
             on_failure=print
             ):
    entries_text = "\n\n".join(map(str, entries))

    params = f"""
    the would be {theme} tweets for {area}
    in a {tone} tone.
    do not include any hashtags.
    """
    if keywords:
        params += "\nthey should include the following keywords: " + str(keywords)

    if hashtags:
        params.replace("do not include any hashtags.", "also include these hashtags: " + str(keywords))
    try:
        chat_completion = client.chat.completions.create(
            messages=[
                {
                    "role": "system",
                    "content": f"You summaraize user's entries to generate Twitter only {num} post{'s' if num != 1 else ''}.\n"
                               f"\n You respond in json objects following this schema: {json.dumps(schema, indent=2)}"
                },
                {
                    "role": "user",
                    "content": f"These are my entries: \n{entries_text}",
                },
                {
                    "role": "assistant",
                    "content": params,
                }
            ],
            model="llama3-70b-8192",
            # response_format={"type": "json_object"},

            # Controls randomness: lowering results in less random completions.
            # As the temperature approaches zero, the model will become deterministic
            # and repetitive.
            temperature=0.75,
        )
    except Exception as e:
        on_failure(e)
        # return

    # callback(chat_completion.choices[0].message.content)
    callback(f"[{json.dumps(schema, indent=2)}]")
