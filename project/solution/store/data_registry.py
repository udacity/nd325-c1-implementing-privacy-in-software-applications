#
# This file is the interface between the stores and the database
#

import sqlite3
from sqlite3 import Connection

from typing import List

from solution.objects.candidate import Candidate


class VotingStore:
    """
    A singleton class that encapsulates the interface between the stores and the databases.

    To use, simply do:

    >>> voting_store = VotingStore.get_instance()   # this will create the stores, if they haven't been created
    >>> voting_store.add_candidate(...)  # now, you can call methods that you need here
    """

    voting_store_instance = None

    @staticmethod
    def get_instance():
        if not VotingStore.voting_store_instance:
            VotingStore.voting_store_instance = VotingStore()

        return VotingStore.voting_store_instance

    def __init__(self):
        """
        DO NOT call this method directly - instead use the VotingStore.get_instance method above.
        """
        self.connection = VotingStore._get_sqlite_connection()
        self.create_tables()

    @staticmethod
    def _get_sqlite_connection() -> Connection:
        return sqlite3.connect(":memory:", check_same_thread=False)

    def create_tables(self):
        print("Creating Tables")
        self.connection.execute(
            '''CREATE TABLE candidates (candidate_id integer primary key autoincrement, name text)''')
        # TODO: Add additional tables here, as you see fit
        self.connection.commit()

    def add_candidate(self, candidate_name: str):
        """
        Adds a candidate into the candidate table, overwriting an existing entry if one exists
        """
        self.connection.execute('''INSERT INTO candidates (name) VALUES ("{0}")'''.format(candidate_name))
        self.connection.commit()

    def get_candidate(self, candidate_id: str) -> Candidate:
        """
        Returns the candidate specified, if that candidate is registered. Otherwise returns None.
        """
        cursor = self.connection.cursor()
        cursor.execute('''SELECT * FROM candidates WHERE candidate_id={0}'''.format(candidate_id))
        candidate_row = cursor.fetchone()
        candidate = Candidate(candidate_id, candidate_row[1]) if candidate_row else None
        self.connection.commit()

        return candidate

    def get_all_candidates(self) -> List[Candidate]:
        cursor = self.connection.cursor()
        cursor.execute('''SELECT * FROM candidates''')
        all_candidate_rows = cursor.fetchall()
        all_candidates = [Candidate(str(candidate_row[0]), candidate_row[1]) for candidate_row in all_candidate_rows]
        self.connection.commit()

        return all_candidates


