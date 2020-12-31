#
# This file is the interface between the stores and the database
#

import sqlite3
from sqlite3 import Connection

from typing import List

from backend.main.objects.candidate import Candidate
from backend.main.objects.voter import MinimalVoter, VoterStatus, BallotStatus
from backend.main.objects.ballot import Ballot
from collections import Counter


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

    @staticmethod
    def refresh_instance():
        """
        DO NOT MODIFY THIS METHOD
        Only to be used for testing. This will only work if the sqlite connection is :memory:
        """
        if VotingStore.voting_store_instance:
            VotingStore.voting_store_instance.connection.close()
        VotingStore.voting_store_instance = VotingStore()

    def __init__(self):
        """
        DO NOT MODIFY THIS METHOD
        DO NOT call this method directly - instead use the VotingStore.get_instance method above.
        """
        self.connection = VotingStore._get_sqlite_connection()
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
            """CREATE TABLE candidates (candidate_id integer primary key autoincrement, name text)""")
        self.connection.execute(
            """CREATE TABLE voters
                (obfuscated_national_id text primary key, first_name text, last_name text, status text)""")
        self.connection.execute(
            """CREATE TABLE valid_ballots (ballot_number text primary key)""")
        self.connection.execute(
            """CREATE TABLE cast_ballots (ballot_number text primary key, chosen_candidate_id integer, comment text)""")
        self.connection.commit()

    def issue_ballot(self, ballot_number: str):
        self.connection.execute("""INSERT INTO valid_ballots (ballot_number) VALUES (?)""", (ballot_number, ))
        self.connection.commit()

    def invalidate_ballot(self, ballot_number: str):
        if not self.ballot_has_been_cast(ballot_number):
            self.connection.execute(
                """DELETE FROM valid_ballots WHERE ballot_number=?""", (ballot_number, ))
            self.connection.commit()

    def cast_ballot(self, obfuscated_national_id: str, ballot: Ballot) -> BallotStatus:
        voter_status = self.get_voter_status(obfuscated_national_id)
        if voter_status == VoterStatus.NOT_REGISTERED:
            return BallotStatus.VOTER_NOT_REGISTERED
        elif not self.ballot_exists(ballot.ballot_number):
            return BallotStatus.INVALID_BALLOT
        elif self.get_voter_status(obfuscated_national_id) != VoterStatus.REGISTERED_NOT_VOTED:
            self._update_voter_status(obfuscated_national_id, VoterStatus.FRAUD_COMMITTED)
            self.connection.commit()
            return BallotStatus.FRAUD_COMMITTED
        else:
            self.connection.execute(
                """
                INSERT INTO cast_ballots (ballot_number, chosen_candidate_id, comment) VALUES (?, ?, ?)
                """, (ballot.ballot_number, ballot.chosen_candidate_id, ballot.voter_comments))
            self._update_voter_status(obfuscated_national_id, VoterStatus.BALLOT_COUNTED)
            self.connection.commit()
            return BallotStatus.BALLOT_COUNTED

    def get_all_comments(self):
        cursor = self.connection.cursor()
        cursor.execute("""SELECT comment FROM cast_ballots""")
        all_comment_rows = cursor.fetchall()
        all_comments = [comment_row[0] for comment_row in all_comment_rows if len(comment_row) != 0]
        self.connection.commit()

        return all_comments

    def _update_voter_status(self, obfuscated_national_id: str, new_status: VoterStatus):
        """
        DO NOT USE outside this class
        """
        self.connection.execute(
            """
            UPDATE voters SET status=? WHERE obfuscated_national_id=?
            """, (new_status.value, obfuscated_national_id)
        )

    def ballot_exists(self, ballot_number: str) -> bool:
        """
        Verifies that a ballot exists
        """
        cursor = self.connection.cursor()
        cursor.execute("""SELECT * FROM valid_ballots WHERE ballot_number=?""", (ballot_number, ))
        exists = cursor.fetchone() is not None
        self.connection.commit()
        return exists

    def ballot_has_been_cast(self, ballot_number: str) -> bool:
        """
        Checks if a ballot has been cast
        """
        cursor = self.connection.cursor()
        cursor.execute("""SELECT * FROM cast_ballots WHERE ballot_number=?""", (ballot_number, ))
        has_been_cast = cursor.fetchone() is not None
        self.connection.commit()
        return has_been_cast

    def add_voter_to_registry(self, voter: MinimalVoter):
        self.connection.execute(
            """INSERT INTO voters
                (obfuscated_national_id, first_name, last_name, status)
                VALUES (?, ?, ?, ?)""",
            (voter.obfuscated_national_id, voter.first_name, voter.last_name, VoterStatus.REGISTERED_NOT_VOTED.value))
        self.connection.commit()

    def get_voter_from_registry(self, obfuscated_national_id: str) -> MinimalVoter:
        cursor = self.connection.cursor()
        cursor.execute("""SELECT * FROM voters WHERE obfuscated_national_id=?""", (obfuscated_national_id,))
        voter_row = cursor.fetchone()
        voter = MinimalVoter(voter_row[1], voter_row[2], obfuscated_national_id) if voter_row else None
        self.connection.commit()

        return voter

    def get_voter_status(self, obfuscated_national_id: str) -> VoterStatus:
        cursor = self.connection.cursor()
        cursor.execute("""SELECT * FROM voters WHERE obfuscated_national_id=?""", (obfuscated_national_id,))
        voter_row = cursor.fetchone()
        status = VoterStatus(voter_row[3]) if voter_row else VoterStatus.NOT_REGISTERED
        self.connection.commit()

        return status

    def remove_voter_from_registry(self, obfuscated_national_id: str):
        self.connection.execute(
            """DELETE FROM voters WHERE obfuscated_national_id=?""", (obfuscated_national_id,))
        self.connection.commit()

    def get_election_winner(self) -> Candidate:
        """
        Gets the vote tally for each candidate
        """
        cursor = self.connection.cursor()
        cursor.execute("""SELECT chosen_candidate_id FROM cast_ballots""")
        all_votes = [row[0] for row in cursor.fetchall()]
        highest_vote_total_id = Counter(all_votes).most_common(1)[0][0]
        cursor.execute("""SELECT * FROM candidates WHERE candidate_id=?""", (highest_vote_total_id,))
        candidate_row = cursor.fetchone()
        candidate = Candidate(str(highest_vote_total_id), candidate_row[1]) if candidate_row else None
        self.connection.commit()
        return candidate

    def get_all_fraudsters(self) -> List[MinimalVoter]:
        cursor = self.connection.cursor()
        cursor.execute(
            """SELECT * FROM voters WHERE status=?""",
            (VoterStatus.FRAUD_COMMITTED.value,))
        fraudsters = cursor.fetchall()
        fraudulent_voters = [MinimalVoter(fraudster[1], fraudster[2], fraudster[0]) for fraudster in fraudsters]
        self.connection.commit()

        return fraudulent_voters

    def add_candidate(self, candidate_name: str):
        """
        Adds a candidate into the candidate table, overwriting an existing entry if one exists
        """
        self.connection.execute("""INSERT INTO candidates (name) VALUES (?)""", (candidate_name,))
        self.connection.commit()

    def get_candidate(self, candidate_id: str) -> Candidate:
        """
        Returns the candidate specified, if that candidate is registered. Otherwise returns None.
        """
        cursor = self.connection.cursor()
        cursor.execute("""SELECT * FROM candidates WHERE candidate_id=?""", (candidate_id,))
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
