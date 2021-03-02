#
# This file is the interface between the stores and the database
#

import sqlite3
from sqlite3 import Connection

from typing import Optional


class User:
    def __init__(self, full_name: str, email: str, user_id: int):
        self.full_name = full_name
        self.email = email
        self.user_id = user_id


class UserStore:
    """
    A singleton class that encapsulates the interface between the stores and the databases.

    To use, simply do:

    >>> user_store = UserStore.get_instance()   # this will create the store
    >>> user_store.add_user(...)  # now, you can call methods that you need here
    """

    user_store_instance = None

    @staticmethod
    def get_instance():
        if not UserStore.user_store_instance:
            UserStore.user_store_instance = UserStore()

        return UserStore.user_store_instance

    @staticmethod
    def refresh_instance():
        if UserStore.user_store_instance:
            UserStore.user_store_instance.connection.close()
        UserStore.user_store_instance = UserStore()

    def __init__(self):
        self.connection = UserStore._get_sqlite_connection()
        self.create_tables()

    @staticmethod
    def _get_sqlite_connection() -> Connection:
        return sqlite3.connect(":memory:", check_same_thread=False)

    def create_tables(self):
        """
        Creates Tables
        """
        self.connection.execute(
            """
            CREATE TABLE users (user_id integer primary key autoincrement, name text, email text)
            """)
        self.connection.commit()

    def add_user(self, user_name: str, user_email: str) -> int:
        """
        Adds a user into the user table, overwriting an existing entry if one exists
        """
        cursor = self.connection.cursor()
        cursor.execute(
            """
            INSERT INTO users (name, email, soft_deleted) VALUES (?, ?, 0)
            """, (user_name, user_email))
        self.connection.commit()
        return cursor.lastrowid

    def get_user(self, user_id: int) -> Optional[User]:
        """
        Returns the user specified, if that user is registered. Otherwise returns None.
        """
        cursor = self.connection.cursor()
        cursor.execute(
            """
            SELECT * FROM users WHERE user_id=?
            """, (user_id,))
        user_row = cursor.fetchone()
        self.connection.commit()
        if not user_row or user_row[3] == 1:
            return None

        return User(user_row[1], user_row[2], user_id) if user_row else None

    def soft_delete_user(self, user_id: int):
        """
        Soft Deletes a user
        """
        raise NotImplementedError()

    def hard_delete_user(self, user_id: int):
        """
        Completely deletes the user from the application-layer.
        """
        raise NotImplementedError()

    def data_subject_access_request(self, user_id: int) -> Optional[User]:
        """
        Gets the data subject. If the user has been soft deleted, will still return the
        user. See the get_user method for inspiration.
        """
        raise NotImplementedError()

