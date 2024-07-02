from database import Entry, wrap_dt, am_pm
from datetime import datetime
from keyboard import write


def tags_entry(content: str):
    tag_starting_list = content.split("%%")
    tags = []
    content_lines = []
    for line in tag_starting_list:
        if line:
            first_space = line.find(" ")
            if first_space == -1:
                first_space = len(line)
            tags.append(line[:first_space].replace("_", " "))
            content_lines.append(line[first_space+1:])
    return tags, "".join(content_lines)


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
    content = input("\t\t")
    if not content:
        exit()
    Entry(tags=tags, content=content).save()
    print()
