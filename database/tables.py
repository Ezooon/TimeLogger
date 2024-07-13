from .db_api import *
from datetime import datetime
from utils import am_pm


class Tags(DBTable):
    default_values = {
        "id": 0,
        "tag": "",
        "color": '2EC7FF',
    }

    def __init__(self, name="", default_values=None):
        super().__init__(name, default_values)
        self.all = dict()

    def update_all(self):
        self.all = dict()
        ts = self.get_items()
        for t in ts:
            self.all[t.tag] = t


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


Tag.table = Tag().table  # ToDo fix: I need those here because the table item_cls, find a better way to initialize them.
Tag.table.update_all()


class Attachment(Item):
    table = DBTable(name="attachments", default_values={
        "id": 0,
        "path": "",
        "entry_id": 0,
        "post_id": 0,
    })

    def __repr__(self):
        return self.path


Attachment.table = Attachment().table


class Entries(DBTable):
    default_values = {
        "id": 0,
        "timestamp": None,
        "content": "",
    }

    def get_items(self, search_params=None, order_by="timestamp", where=None, tags_in=None, tags_out=None, **e_where):
        if tags_in:
            id_tuples = db_api.read("entries_tags", where=[("tag_id", "in", db_tuple(tags_in))])
            where.append(("id", "in", db_tuple(i_tup[0] for i_tup in id_tuples)))

        if tags_out:
            id_tuples = db_api.read("entries_tags", where=[("tag_id", "in", db_tuple(tags_out))])
            where.append(("id", "not in", db_tuple(i_tup[0] for i_tup in id_tuples)))

        return super().get_items(search_params, order_by, where, **e_where)

    def check_values(self, raw_values):
        if "timestamp" in raw_values:
            raw_values['timestamp'] = datetime.fromisoformat(raw_values['timestamp'])
        return raw_values


class Entry(Item):
    table = Entries()

    def __init__(self, in_db=False, attachments=set(), tags=None, **fields):
        super().__init__(in_db, **fields)

        if self.in_db:
            self.tags = self.get_tags()
            self.attachments = self.get_attachments()
        else:
            self.tags = set()  # quotes
            self.attachments = set()

        self.current_tags = tags or map(str, self.tags)
        self.current_attachments = set(Attachment(path=att, entry_id=self.id) for att in attachments) or self.attachments

    def new_attachments(self, attachments):
        """a way to change the entry's attachments"""

        self.current_attachments = set(
            Attachment(path=att, entry_id=self.id) for att in attachments) or self.attachments

    def get_tags(self):
        tag_ids = tuple(entry_tag[1] for entry_tag in db_api.read("entries_tags", entry_id=self.id))
        return set(Tag().table.get_items(where=[('id', "in", db_tuple(tag_ids))]))

    def get_attachments(self):
        attachments = Attachment.table.get_items(entry_id=self.id)
        return attachments

    def validate(self, fields_values):
        if not self.timestamp:
            fields_values["timestamp"] = datetime.now().replace(microsecond=0)
        return fields_values

    def save_tags(self):
        tag_list = set(map(str, self.tags))
        new_tag_list = set(self.current_tags)
        # new_tag_list = set(map(Tag.add_or_get_tag, filter(bool, self.current_tags)))
        to_add = set(map(Tag.add_or_get_tag, (new_tag_list - tag_list)))
        to_delete = set(map(Tag.add_or_get_tag, (tag_list - new_tag_list)))
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
            attachment.entry_id = self.id
            attachment.save()
        for attachment in to_delete:
            attachment.delete()

    def on_saved(self):
        self.save_tags()
        self.save_attachments()

    def __repr__(self):
        tags = [str(tag) for tag in self.current_tags]
        return f"\t{am_pm(self.timestamp)}: {' '.join(tags)}\n\t\t{self.content}"

    def __str__(self):
        tags = [str(tag) for tag in self.current_tags]
        return f"\t{self.timestamp}: {' '.join(tags)}\n\t\t{self.content}"


Entry.table = Entry().table


class Posts(DBTable):
    default_values = {
        "id": 0,
        "timestamp": None,
        "content": "",
        "linkedin": False,
        "twitter": False,
        "facebook": False,
    }

    def get_items(self, search_params=None, order_by="timestamp", where=None, **e_where):
        return super().get_items(search_params, order_by, where, **e_where)

    def check_values(self, raw_values):
        if "timestamp" in raw_values:
            raw_values['timestamp'] = datetime.fromisoformat(raw_values['timestamp'])
        return raw_values


class Post(Item):
    table = Posts()

    def __init__(self, in_db=False, attachments=set(), **fields):
        super().__init__(in_db, **fields)

        if self.in_db:
            self.attachments = self.get_attachments()
        else:
            self.attachments = set()

        self.current_attachments = set(Attachment(path=att, entry_id=self.id) for att in attachments) or self.attachments

    def new_attachments(self, attachments):
        """a way to change the entry's attachments"""

        self.current_attachments = set(
            Attachment(path=att, entry_id=self.id) for att in attachments) or self.attachments

    def get_attachments(self):
        attachments = Attachment.table.get_items(entry_id=self.id)
        return attachments

    def validate(self, fields_values):
        if not self.timestamp:
            fields_values["timestamp"] = datetime.now().replace(microsecond=0)
        return fields_values

    def save_attachments(self):
        attachment_list = set(self.attachments)
        new_attachment_list = set(self.current_attachments)
        to_add = new_attachment_list - attachment_list
        to_delete = attachment_list - new_attachment_list

        for attachment in to_add:
            attachment.entry_id = self.id
            attachment.save()
        for attachment in to_delete:
            attachment.delete()

    def on_saved(self):
        self.save_attachments()

    def __repr__(self):
        return f"\t{am_pm(self.timestamp)}:\n\t\t{self.content}"


Post.table = Post().table


# ToDo have the posts table include fields to reference the entries used to generate it.
