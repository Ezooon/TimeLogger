from database import Entry, wrap_dt, am_pm
from datetime import datetime
from keyboard import write


def tags_entry(content: str):
    tag_starting_list = content.split("%%")
    tags = []
    content_lines = [] if content.startswith("%%") else [tag_starting_list.pop(0)]
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
    last_tags += (" " + " ".join(more_tags))
    if not content:
        exit()
    Entry(tags=list(set(tags + more_tags)), content=content).save()
    # print("tags:", tags, "more tags:", more_tags, "content:", content)
    print()
