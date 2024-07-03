from PIL import ImageGrab
from os.path import join, exists
from database import Entry, wrap_dt, am_pm
from datetime import datetime
from keyboard import write


def tags_entry(content: str, scape_char="%%"):
    tag_starting_list = content.split(scape_char)
    tags = []
    content_lines = [] if content.startswith(scape_char) else [tag_starting_list.pop(0)]
    for line in tag_starting_list:
        if line:
            first_space = line.find(" ")
            if first_space == -1:
                first_space = len(line)
            tags.append(line[:first_space])
            content_lines.append(line[first_space+1:])
    return tags, "".join(content_lines or content)


today_logs = Entry().table.get_items(where=[("timestamp", ">=", wrap_dt(datetime.today().date()))])
print(str(datetime.today().date()) + ": \n")
for log in today_logs:
    print(log, "\n")

last_tags = ""
while True:
    print(f"\t{am_pm(datetime.now())}: ", end="")
    write(last_tags)
    last_tags = input()
    tags = last_tags.split(" ")
    more_tags, content = tags_entry(input("\t\t"))
    attachments, content = tags_entry(content, "**")
    last_tags += (" " + " ".join(more_tags))
    if not content:
        exit()

    if "clp" in attachments:
        im = ImageGrab.grabclipboard()
        if im:
            img_path = join("from_clipboard", str(datetime.now().replace(microsecond=0)).replace(":", "") + ".png")
            open(img_path, "wb").close()
            im.save(img_path, format="png")
            attachments.append(img_path)

    attachments = list(filter(exists, attachments))

    Entry(tags=list(set(tags + more_tags)), content=content, attachments=attachments).save()
    # print("tags:", tags, "more tags:", more_tags, "content:", content, "attachments:", attachments)
    print()
