from .db_api import *
from datetime import datetime
from utils import am_pm


class Tags(DBTable):
    default_values = {
        "id": 0,
        "tag": "",
        "color": '2EC7FF',
    }
    all = {}


class Tag(Item):
    table = Tags()

    @classmethod
    def add_or_get_tag(self, tag):
        if tag not in self.table.all:
            tag = Tag(tag=tag)
            tag.save()
            self.table.all[tag.tag] = tag
        else:
            tag = self.table.all[tag]
        return tag

    def __repr__(self):
        return self.tag


ts = db_api.read('tags')
for t in ts:
    Tags.all[t[1]] = Tag(True, id=t[0], tag=t[1], color=t[2])


Tag.table = Tag().table


class Entries(DBTable):
    default_values = {
        "id": 0,
        "timestamp": datetime.now().replace(microsecond=0),
        "content": "",
    }

    def check_values(self, raw_values):
        if "timestamp" in raw_values:
            raw_values['timestamp'] = datetime.fromisoformat(raw_values['timestamp'])
        return raw_values


class Entry(Item):
    table = Entries()

    def __init__(self, in_db=False, tags=[], **fields):
        super().__init__(in_db, **fields)
        self.tags = set()
        if self.in_db:
            self.tags = self.get_tags()
        self.current_tags = tags or map(str, self.tags)

    def get_tags(self):
        tag_ids = tuple(entry_tag[1] for entry_tag in db_api.read("entries_tags", entry_id=self.id))
        return set(Tag().table.get_items(where=[('id', "in", db_tuple(tag_ids))]))

    def validate(self, fields_values):
        fields_values["timestamp"] = datetime.now().replace(microsecond=0)
        return fields_values

    def on_saved(self):
        tag_list = self.tags
        new_tag_list = set(map(Tag.add_or_get_tag, self.current_tags))
        to_add = new_tag_list - tag_list
        to_delete = tag_list - new_tag_list
        for tag in to_add:
            db_api.create("entries_tags", entry_id=self.id, tag_id=tag.id)
        for tag in to_delete:
            db_api.delete("entries_tags", entry_id=self.id, tag_id=tag.id)

    def __repr__(self):
        tags = [str(tag) for tag in self.current_tags]
        return f"\t{am_pm(self.timestamp)}: {' '.join(tags)}\n\t\t{self.content}"


Entry.table = Entry().table

