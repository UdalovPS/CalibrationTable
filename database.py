import sqlite3 as sq

class DataBase():
    def __init__(self, db_name='db.db'):
        self.db_name = db_name

    def open_db(self):
        con = sq.connect(self.db_name)
        return con

    def close_db(self):
        self.open_db().close()

    def make_table(self, table_name, fields):
        con = self.open_db()
        cur = con.cursor()
        cur.execute("""CREATE TABLE IF NOT EXISTS {0} ({1})""".format(table_name,
                                                                      fields))
        con.commit()
        con.close()

    def _delete_table(self, table_name):
        cur = self.open_db().cursor()
        cur.execute("""DROP TABLE IF EXISTS {0}""".format(table_name))
        self.close_db()

    def insert_in_table(self, table_name, data_fields=None, data=None):
        con = self.open_db()
        cur = con.cursor()
        if data:
            cur.execute("""INSERT INTO {0} ({1}) VALUES {2};""".format(table_name,
                                                                         data_fields, data))
        else:
            cur.execute("""INSERT INTO {0} DEFAULT VALUES ;""".format(table_name))
        con.commit()
        con.close()

    def select_from_db(self, table_name, cond=None, field=None):
        con = self.open_db()
        cur = con.cursor()
        if not cond:
            cur.execute("""SELECT {1} FROM {0}""".format(table_name, field))
        else:
            cur.execute("""SELECT {2} FROM {0} WHERE {1}""".format(table_name,
                                                                   cond, field))
        con.commit()
        data = cur.fetchall()
        con.close()
        return data

    def join_from_db(self, field, main_table, sub_table, cond):
        con = self.open_db()
        cur = con.cursor()
        cur.execute("""SELECT {0} FROM {1} JOIN {2} ON {3}""".format(field, main_table,
                                                                     sub_table, cond))
        con.commit()
        data = cur.fetchall()
        con.close()
        return data

    def delete_from_db(self, table_name, conditions):
        con = self.open_db()
        cur = con.cursor()
        cur.execute("""DELETE FROM {0} WHERE {1}""".format(table_name, conditions))
        con.commit()
        con.close()

    def update_field(self, table_name, field, cond):
        con = self.open_db()
        cur = con.cursor()
        # print(table_name, field, cond)
        cur.execute("""UPDATE {0} SET {1} WHERE {2}""".format(table_name, field, cond))
        con.commit()
        con.close()

    def insert_many(self, table_name, data):
        con = self.open_db()
        cur = con.cursor()
        cur.executemany("INSERT INTO {0} VALUES(?, ?)".format(table_name), data)
        con.commit()
        con.close()

class AddDataTable(DataBase):
    def __init__(self):
        DataBase.__init__(self)
        self.table_with_names = 'names'
        self.names_table_fields = 'codName TEXT, name TEXT'
        self.names_data_fields = 'codName, name'
        self.table_with_density = 'product'
        self.prod_table_fields = 'prodName TEXT, density REAL'
        self.prod_data_fields = 'prodName, density'

        self.make_table(self.table_with_names, self.names_table_fields)
        self.make_table(self.table_with_density, self.prod_table_fields)


if __name__ == '__main__':
    # a = DataBase()._delete_table('test')
    # a = DataBase()
    # a.make_table('test', 'level REAL, volume REAL')
    # a.insert_many('test', ((0.1, 0.2), (0.3, 0.4)))
    pass
