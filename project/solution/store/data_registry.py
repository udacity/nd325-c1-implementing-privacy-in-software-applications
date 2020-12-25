#
# This file is the interface between the stores and the database
#

import sqlite3
from sqlite3 import Connection
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
        self.create_tables()

    def _get_sqlite_connection(self) -> Connection:
        return sqlite3.connect(":memory:")

    def create_tables(self):
        connection = self._get_sqlite_connection()
        connection.execute('''CREATE TABLE candidates (candidate_id text, name text)''')
        # TODO: Add additional tables here, as you see fit
        connection.commit()
        connection.close()

    def add_candidate(self, candidate: Candidate):
        """
        Adds a candidate into the candidate table, overwriting an existing entry if one exists
        """
        connection = self._get_sqlite_connection()
        connection.execute('''INSERT INTO candidates ({0}, {1})'''.format(
            candidate.candidate_id, candidate.name))
        connection.commit()
        connection.close()

    def get_candidate(self, candidate_id: str) -> Candidate:
        """
        Returns the candidate specified, if that candidate is registered. Otherwise returns None.
        """
        connection = self._get_sqlite_connection()
        cursor = connection.cursor()
        cursor.execute('''SELECT * FROM candidates WHERE candidate_id={0}'''.format(candidate_id))
        candidate_row = cursor.fetchone()
        candidate = Candidate(candidate_id, candidate_row[1]) if candidate_row else None
        connection.commit()
        connection.close()

        return candidate
