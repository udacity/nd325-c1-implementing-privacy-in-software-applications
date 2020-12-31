#
# This file is the interface between the stores and the database
#

import sqlite3
from sqlite3 import Connection

from typing import List

from backend.main.objects.candidate import Candidate
from backend.main.objects.voter import MinimalVoter, VoterStatus


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
        """
        Creates Tables
        """
        self.connection.execute(
            """CREATE TABLE candidates (candidate_id integer primary key autoincrement, name text)""")
        self.connection.execute(
            """CREATE TABLE voters
                (obfuscated_national_id text primary key, first_name text, last_name text, status text)""")
        self.connection.commit()

    def add_voter_to_registry(self, voter: MinimalVoter):
        self.connection.execute(
            """INSERT INTO voters
                (obfuscated_national_id, first_name, last_name, status)
                VALUES ("{0}", "{1}", "{2}", "{3}")""".format(
                voter.obfuscated_national_id,
                voter.first_name,
                voter.last_name,
                VoterStatus.REGISTERED_NOT_VOTED.value))
        self.connection.commit()

    def get_voter_from_registry(self, obfuscated_national_id: str) -> MinimalVoter:
        cursor = self.connection.cursor()
        cursor.execute("""SELECT * FROM voters WHERE obfuscated_national_id='{0}'""".format(obfuscated_national_id))
        voter_row = cursor.fetchone()
        voter = MinimalVoter(voter_row[1], voter_row[2], obfuscated_national_id) if voter_row else None
        self.connection.commit()

        return voter

    def get_voter_status(self, obfuscated_national_id: str) -> VoterStatus:
        cursor = self.connection.cursor()
        cursor.execute("""SELECT * FROM voters WHERE obfuscated_national_id='{0}'""".format(obfuscated_national_id))
        voter_row = cursor.fetchone()
        status = VoterStatus(voter_row[3]) if voter_row else VoterStatus.NOT_REGISTERED
        self.connection.commit()

        return status

    def remove_voter_from_registry(self, obfuscated_national_id: str):
        self.connection.execute(
            """DELETE FROM voters WHERE obfuscated_national_id='{0}'""".format(obfuscated_national_id))
        self.connection.commit()

    def add_candidate(self, candidate_name: str):
        """
        Adds a candidate into the candidate table, overwriting an existing entry if one exists
        """
        self.connection.execute("""INSERT INTO candidates (name) VALUES ('{0}')""".format(candidate_name))
        self.connection.commit()

    def get_candidate(self, candidate_id: str) -> Candidate:
        """
        Returns the candidate specified, if that candidate is registered. Otherwise returns None.
        """
        cursor = self.connection.cursor()
        cursor.execute("""SELECT * FROM candidates WHERE candidate_id='{0}'""".format(candidate_id))
        candidate_row = cursor.fetchone()
        candidate = Candidate(candidate_id, candidate_row[1]) if candidate_row else None
        self.connection.commit()

        return candidate

    def get_all_candidates(self) -> List[Candidate]:
        """
        Gets ALL the candidates from the database
        """
        cursor = self.connection.cursor()
        cursor.execute("""SELECT * FROM candidates""")
        all_candidate_rows = cursor.fetchall()
        all_candidates = [Candidate(str(candidate_row[0]), candidate_row[1]) for candidate_row in all_candidate_rows]
        self.connection.commit()

        return all_candidates
