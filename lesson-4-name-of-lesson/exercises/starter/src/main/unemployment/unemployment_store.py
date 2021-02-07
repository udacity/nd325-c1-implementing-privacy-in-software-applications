#
# This file is the interface between the stores and the database
# DO NOT MODIFY THIS FILE
#

import sqlite3
from sqlite3 import Connection
from typing import Set

from src.main.unemployment.privacy import encrypt_incarceration_status, decrypt_incarceration_status


class UnemploymentStore:
    """
    A singleton class that encapsulates the interface between the stores and the databases.

    To use, simply do:

    >>> voting_store = UnemploymentStore.get_instance()   # this will create the stores, if they haven't been created
    >>> voting_store.add_candidate(...)  # now, you can call methods that you need here
    """

    voting_store_instance = None

    @staticmethod
    def get_instance():
        if not UnemploymentStore.voting_store_instance:
            UnemploymentStore.voting_store_instance = UnemploymentStore()

        return UnemploymentStore.voting_store_instance

    @staticmethod
    def refresh_instance():
        """
        DO NOT MODIFY THIS METHOD
        Only to be used for testing. This will only work if the sqlite connection is :memory:
        """
        if UnemploymentStore.voting_store_instance:
            UnemploymentStore.voting_store_instance.connection.close()
        UnemploymentStore.voting_store_instance = UnemploymentStore()

    def __init__(self):
        """
        DO NOT MODIFY THIS METHOD
        DO NOT call this method directly - instead use the UnemploymentStore.get_instance method above.
        """
        self.connection = UnemploymentStore._get_sqlite_connection()
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
            """
            CREATE TABLE unemployed (obfuscated_national_id text, obfuscated_email_address text, incarcerated text)
            """
        )
        self.connection.commit()

    def mark_citizen_as_unemployed(
            self, obfuscated_national_id: str, obfuscated_email_address: str, incarcerated: bool):
        """
        Adds a unemployed citizen into the unemployed table
        """
        self.connection.execute(
            """INSERT INTO unemployed (obfuscated_national_id, obfuscated_email_address, incarcerated) VALUES (?)""",
            (obfuscated_national_id, obfuscated_email_address, encrypt_incarceration_status(incarcerated)))
        self.connection.commit()

    def verify_citizen_is_incarcerated(self, obfuscated_national_id: str) -> bool:
        """
        If the citizen with the given national id is in the unemployed table, returns true. Otherwise returns false.
        """
        cursor = self.connection.cursor()
        cursor.execute(
            """SELECT incarcerated FROM unemployed WHERE obfuscated_national_id=?""", (obfuscated_national_id,))
        citizen_row = cursor.fetchone()
        self.connection.commit()

        return citizen_row is not None and decrypt_incarceration_status(citizen_row[0])

    def verify_candidate_is_unemployed(self, obfuscated_national_id: str) -> bool:
        """
        If the citizen with the given national id is in the unemployed table, returns true. Otherwise returns false.
        """
        cursor = self.connection.cursor()
        cursor.execute("""SELECT * FROM unemployed WHERE obfuscated_national_id=?""", (obfuscated_national_id,))
        citizen_row = cursor.fetchone()
        self.connection.commit()

        return citizen_row is not None

    def unmark_citizen_as_unemployed(self, obfuscated_national_id: str):
        """
        If the citizen with the given national id is in the unemployed table deletes it.
        """
        self.connection.execute(
            """DELETE FROM unemployed WHERE obfuscated_national_id=?""", (obfuscated_national_id,))
        self.connection.commit()

    def get_all_email_addresses(self) -> Set[str]:
        """
        Gets all the obfuscated email addresses of all the unemployed individuals in the database.
        :return: A set of obfuscated email addresses
        """
        cursor = self.connection.cursor()
        cursor.execute("""SELECT obfuscated_email_address FROM unemployed""")
        all_phone_numbers = cursor.fetchall()
        self.connection.commit()

        return {x[0] for x in all_phone_numbers}

