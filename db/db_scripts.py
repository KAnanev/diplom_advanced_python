import sqlite3 as sl
import sys
import traceback

from sqlite3 import Error


def error_db(old_function):
    def new_function(self, *args, **kwargs):
        try:
            return old_function(self, *args, **kwargs)
        except Error as er:
            print('SQLite error: %s' % (' '.join(er.args)))
            print("Exception class is: ", er.__class__)
            print('SQLite traceback: ')
            exc_type, exc_value, exc_tb = sys.exc_info()
            print(traceback.format_exception(exc_type, exc_value, exc_tb))

    return new_function


class DB:
    def __init__(self):
        self.con = sl.connect('db/users.db')

    def __enter__(self):
        self.cursor_obj = self.con.cursor()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.con.close()

    @error_db
    def create_db(self):
        self.cursor_obj.executescript("""
                        CREATE TABLE if not exists main_users(
                        id integer PRIMARY KEY AUTOINCREMENT,
                        main_user integer UNIQUE);
                        CREATE TABLE if not exists target_users(
                        id integer PRIMARY KEY AUTOINCREMENT,
                        main_user_id integer REFERENCES main_users (id),
                        target_user integer UNIQUE);
                        """)
        self.con.commit()

    @error_db
    def select_main_user(self, main_user_id):
        re = self.cursor_obj.execute("""
                            SELECT * from main_users
                            WHERE main_user = (?);""", (main_user_id,))
        result = re.fetchall()
        self.con.commit()
        return result

    @error_db
    def insert_main_user(self, main_user_id):
        self.cursor_obj.execute("""
                            INSERT INTO main_users(
                            main_user)
                            VALUES(?)""", (main_user_id,))

        self.con.commit()

    @error_db
    def select_target_users(self, main_user_id):
        re = self.cursor_obj.execute("""
                                SELECT * from target_users
                                WHERE main_user_id = (?);""", (main_user_id,))
        result = re.fetchall()
        self.con.commit()
        return result

    @error_db
    def insert_target_users(self, main_id, users):
        users_id = []
        for i in users:
            users_id.append((main_id, i))

        self.cursor_obj.executemany("""
                                INSERT INTO target_users(
                                main_user_id,
                                target_user)
                                VALUES(?, ?)""", users_id)

        self.con.commit()
