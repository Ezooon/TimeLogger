import json
from aitool import client


schema = {
    "content": "the tweet's body",
    "suggested images": [
        "a description of a relevant image the user can attach to boost engagement",
        "..."
    ],
}


def generate(entries,
             num="3",  # the number of posts.
             area="dev logs",  # Is it related to a specific industry or niche?
             tone="humorous",
             # Do you have any specific tone or style (e.g. formal, informal, humorous, inspirational)?
             note="",
             keywords=[],  # Are there any specific keywords you'd like to include?
             hashtags=[],  # Are there any specific hashtags you'd like to include?
             callback=print,
             on_failure=print
             ):
    entries_text = "\n\n".join(map(str, entries))

    params = f"""
    write {area} tweets, in a {tone} tone.
    do not include any hashtags.
    """
    if keywords:
        params += "\nthey should include the following keywords: " + str(keywords)

    if hashtags:
        params = params.replace("do not include any hashtags.", "only include these hashtags: " + str(hashtags))

    messages = [
        {
            "role": "system",
            "content": "You're Time Logger an application that let's the user write entries about their day."
                       "You're purpose is to help the user navigate and document their life."
        },
        {
            "role": "system",
            "content": f"You summaraize user's entries and writing style to generate Twitter only {num} post{'s' if num != 1 else ''}.\n"
                       f"\n You respond in no more than json script following this schema: [{json.dumps(schema, indent=4)}]"
        },
        {
            "role": "assistant",
            "content": params,
        },
        {
            "role": "user",
            "content": f"These are my entries: \n{entries_text}",
        },
    ]
    if note:
        messages.append({
            "role": "user",
            "content": f"Note: \n{note}",
        })

    try:
        chat_completion = client.chat.completions.create(
            messages=messages,
            model="mixtral-8x7b-32768",
            # response_format={"type": "json_object"},

            # Controls randomness: lowering results in less random completions.
            # As the temperature approaches zero, the model will become deterministic
            # and repetitive.
            temperature=0.75,
        )
    except Exception as e:
        on_failure(e)
        return

    callback(chat_completion.choices[0].message.content)
