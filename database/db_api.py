from sqlite3 import connect
from os.path import abspath, join, split


def wrap_dt(timestamp):
    return "'" + str(timestamp) + "'"


def db_tuple(values, wrapper=""):
    values = tuple(values)
    if len(values) == 1:
        if callable(wrapper):
            return f"({wrapper(values[0])})"
        return f"({wrapper}{values[0]}{wrapper})"

    if wrapper:
        if callable(wrapper):
            return str(map(wrapper, values))
        else:
            return str(tuple(f"({wrapper}{value}{wrapper})" for value in values))
    return str(values)


db_path = join(*split(__file__)[:-1], "logs.db")


class DBAPI:
    def __init__(self):
        self.conn = connect(db_path)
        self.cur = self.conn.cursor()
        self.close = self.conn.close

    def create(self, table: str, **kwargs):
        keys = list(kwargs.keys())
        values = [value for _, value in kwargs.items()]
        self.cur.execute(f"""INSERT INTO {table}({', '.join(keys)})
                        VALUES ({", ".join(["?"] * len(values))});""", values)
        self.conn.commit()
        return self.read(table)[-1]

    def read(self, table: str, search_params=None, order_by="", where=None, test=False, **e_where):
        if where is None:
            where = []
        if search_params is None:
            search_params = {}

        filters = ""
        non_eq_filters = ""
        search = ""
        if e_where:
            filters = " WHERE " + " AND ".join([f'{op} = ?' for op in e_where])
        if where:
            non_eq_filters = (" AND " if e_where else " WHERE ") + \
                             " AND ".join(
                                 [" ".join(map(str, q_filter)) for q_filter in where]
                             )
        if search_params:
            search = (" AND " if e_where or where else " WHERE ") + \
                     " AND ".join([f"{op} LIKE '%{search_params[op]}%'" for op in search_params])
        if order_by:
            order_by = f" ORDER BY {order_by}"

        line = "SELECT * FROM " + table + filters + non_eq_filters + search + order_by + ";"
        args = [value for _, value in e_where.items()]

        if test:
            print(line, args)

        try:
            self.cur.execute(line, args)
        except Exception as e:
            print(line, args)
            print(e)
            exit()
        return self.cur.fetchall()

    def update(self, table: str, where, **kwargs):
        self.cur.execute(f"UPDATE {table} SET " +
                          ", ".join([f"{key} = ?" for key in kwargs.keys()]) +
                          " WHERE " + ", ".join([f"{key} = ?" for key in where.keys()]) + ";",
                         [value for _, value in kwargs.items()] + [value for _, value in where.items()])
        self.conn.commit()

    def delete(self, table: str, **kwargs):
        self.cur.execute(f"DELETE FROM {table} WHERE " +
                         " AND ".join([f"{key} = ?" for key in kwargs.keys()]) + ";",
                         [value for _, value in kwargs.items()])
        self.conn.commit()

    def bulk_delete(self, table: str, field, values):
        values = tuple(values) if len(values) > 1 else f"({values[0]})"
        self.cur.execute(f"DELETE FROM {table} WHERE {field}  in {values};")
        self.conn.commit()


db_api = DBAPI()


class DBTable:
    default_values = {"id": 0}

    def __init__(self, name="", default_values=None):
        self.name = name or type(self).__name__.lower()
        if default_values:
            type(self).default_values = default_values

    def get_items(self, search_params=None, order_by="", where=None, **e_where):
        data = db_api.read(self.name, search_params, order_by, where, **e_where)
        keys = list(self.default_values.keys())
        items = []
        for i_list in data:
            i_data = {}
            for i in range(len(keys)):
                i_data[keys[i]] = i_list[i]
            items.append(self.item_cls(in_db=True, **self.check_values(i_data)))
        return items

    def check_values(self, raw_values):
        return raw_values


class Item:
    table = DBTable()

    lookup_fields = {"id"}
    """for updating and deleting"""

    def __init__(self, in_db=False, **fields):
        self.table.item_cls = self.__class__
        self.in_db = in_db
        for key, value in self.table.default_values.items():
            setattr(self, key, fields.get(key, value))

    @property
    def fields_values(self):
        fields_values = {}
        for key in self.table.default_values.keys():
            fields_values[key] = getattr(self, key)
        return fields_values

    def validate(self, fields_values):
        return fields_values

    def on_saved(self):
        pass

    def save(self):
        fields_values = self.validate(self.fields_values)
        where = {}
        for field in self.lookup_fields:
            if field in fields_values.keys():
                where[field] = fields_values.pop(field)

        if self.in_db:
            db_api.update(self.table.name, where, **fields_values)
            self.on_saved()
            return

        self.id = db_api.create(self.table.name, **fields_values)[0]
        self.in_db = True
        self.on_saved()

    def delete(self):
        where = {}
        fields_values = self.fields_values
        for field in self.lookup_fields:
            if field in fields_values.keys():
                where[field] = fields_values[field]

        db_api.delete(self.table.name, **where)

