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

    def get_items(self, search_params=None, order_by="timestamp", where=None, tags_in=None, tags_out=None, **e_where):
        if tags_in:
            id_tuples = db_api.read("entries_tags", test=True, where=[("tag_id", "in", db_tuple(tags_in))])
            where.append(("id", "in", db_tuple(i_tup[0] for i_tup in id_tuples)))

        if tags_out:
            id_tuples = db_api.read("entries_tags", test=True, where=[("tag_id", "in", db_tuple(tags_out))])
            where.append(("id", "not in", db_tuple(i_tup[0] for i_tup in id_tuples)))

        return super().get_items(search_params, order_by, where, test=True, **e_where)

    def check_values(self, raw_values):
        if "timestamp" in raw_values:
            raw_values['timestamp'] = datetime.fromisoformat(raw_values['timestamp'])
        return raw_values


class Entry(Item):
    table = Entries()

    def __init__(self, in_db=False, attachments=None, tags=None, **fields):
        super().__init__(in_db, **fields)
        if attachments is None:
            attachments = []
        self.tags = set()
        self.attachments = set()

        if self.in_db:
            self.tags = self.get_tags()
            self.attachments = self.get_attachments()

        self.current_tags = tags or map(str, self.tags)
        self.current_attachments = attachments or self.attachments

    def get_tags(self):
        tag_ids = tuple(entry_tag[1] for entry_tag in db_api.read("entries_tags", entry_id=self.id))
        return set(Tag().table.get_items(where=[('id', "in", db_tuple(tag_ids))]))

    def get_attachments(self):
        attachments = set(att_path for att_id, att_path, *_ in db_api.read("attachments", entry_id=self.id))
        return attachments

    def validate(self, fields_values):
        fields_values["timestamp"] = datetime.now().replace(microsecond=0)
        return fields_values

    def save_tags(self):
        tag_list = self.tags
        new_tag_list = set(map(Tag.add_or_get_tag, self.current_tags))
        # new_tag_list = set(map(Tag.add_or_get_tag, filter(bool, self.current_tags)))
        to_add = new_tag_list - tag_list
        to_delete = tag_list - new_tag_list
        for tag in to_add:
            db_api.create("entries_tags", entry_id=self.id, tag_id=tag.id)
        for tag in to_delete:
            db_api.delete("entries_tags", entry_id=self.id, tag_id=tag.id)

    def save_attachments(self):
        attachment_list = set(self.attachments)
        new_attachment_list = set(self.current_attachments)
        to_add = new_attachment_list - attachment_list
        to_delete = attachment_list - new_attachment_list

        for attachment in to_add:
            db_api.create("attachments", entry_id=self.id, path=attachment)
        for attachment in to_delete:
            db_api.delete("attachments", entry_id=self.id, path=attachment)

    def on_saved(self):
        self.save_tags()
        self.save_attachments()

    def __repr__(self):
        tags = [str(tag) for tag in self.current_tags]
        return f"\t{am_pm(self.timestamp)}: {' '.join(tags)}\n\t\t{self.content}"


Entry.table = Entry().table

