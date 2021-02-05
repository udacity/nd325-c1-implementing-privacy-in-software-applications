#
# This file is the interface between the stores and the database
#

import sqlite3
from sqlite3 import Connection

from typing import List, Optional

from src.main.hiring_candidate import Candidate


class HiringStore:
    """
    A singleton class that encapsulates the interface between the stores and the databases.

    To use, simply do:

    >>> hiring_store = HiringStore.get_instance()   # this will create the stores, if they haven't been created
    >>> hiring_store.add_candidate(...)  # now, you can call methods that you need here
    """

    hiring_store_instance = None

    @staticmethod
    def get_instance():
        if not HiringStore.hiring_store_instance:
            HiringStore.hiring_store_instance = HiringStore()

        return HiringStore.hiring_store_instance

    @staticmethod
    def refresh_instance():
        """
        DO NOT MODIFY THIS METHOD
        Only to be used for testing. This will only work if the sqlite connection is :memory:
        """
        if HiringStore.hiring_store_instance:
            HiringStore.hiring_store_instance.connection.close()
        HiringStore.hiring_store_instance = HiringStore()

    def __init__(self):
        """
        DO NOT MODIFY THIS METHOD
        DO NOT call this method directly - instead use the HiringStore.get_instance method above.
        """
        self.connection = HiringStore._get_sqlite_connection()
        self.create_tables()

    @staticmethod
    def _get_sqlite_connection() -> Connection:
        """
        DO NOT MODIFY THIS METHOD
        """
        return sqlite3.connect(":memory:", check_same_thread=False)

    def create_tables(self):
        """
        Creates Tables
        """
        self.connection.execute(
            """CREATE TABLE candidates (candidate_id integer primary key autoincrement, name text, email text, soft_deleted integer)""")
        self.connection.commit()

    def add_candidate(self, candidate_name: str, candidate_email: str) -> int:
        """
        Adds a candidate into the candidate table, overwriting an existing entry if one exists
        """
        cursor = self.connection.cursor()
        cursor.execute(
            """INSERT INTO candidates (name, email, soft_deleted) VALUES (?, ?, 0)""", (candidate_name, candidate_email))
        self.connection.commit()
        return cursor.lastrowid

    def get_candidate(self, candidate_id: int) -> Optional[Candidate]:
        """
        Returns the candidate specified, if that candidate is registered. Otherwise returns None.
        """
        cursor = self.connection.cursor()
        cursor.execute("""SELECT * FROM candidates WHERE candidate_id=?""", (candidate_id,))
        candidate_row = cursor.fetchone()
        self.connection.commit()
        if not candidate_row or candidate_row[3] == 1:
            return None

        return Candidate(candidate_id, candidate_row[1], candidate_row[2]) if candidate_row else None

    def soft_delete_candidate(self, candidate_id: int):
        """
        Soft Deletes a candidate
        """
        cursor = self.connection.cursor()
        cursor.execute("""UPDATE candidates SET soft_deleted=1 WHERE candidate_id=?""", (candidate_id,))
        candidate_row = cursor.fetchone()
        self.connection.commit()

    def candidate_data_subject_access_request(self, candidate_id: int) -> Optional[Candidate]:
        """
        Gets the data subject. If the candidate has been soft deleted, will still return the candidate. See
        the get_candidate method for inspiration.
        """
        cursor = self.connection.cursor()
        cursor.execute("""SELECT * FROM candidates WHERE candidate_id=?""", (candidate_id,))
        candidate_row = cursor.fetchone()
        self.connection.commit()

        if not candidate_row:
            return None

        return Candidate(candidate_id, candidate_row[1], candidate_row[2])

    def hard_delete_candidate(self, candidate_id: int):
        """
        Completely deletes the candidate from the application-layer.
        """
        self.connection.execute("""DELETE FROM candidates WHERE candidate_id=?""", (candidate_id,))
        self.connection.commit()

    def get_all_candidates(self) -> List[Candidate]:
        """
        Gets ALL the candidates from the database that haven't been soft deleted
        """
        cursor = self.connection.cursor()
        cursor.execute("""SELECT * FROM candidates WHERE soft_deleted=0""")
        all_candidate_rows = cursor.fetchall()
        all_candidates = [
            Candidate(candidate_row[0], candidate_row[1], candidate_row[2])
            for candidate_row in all_candidate_rows
        ]
        self.connection.commit()

        return all_candidates
