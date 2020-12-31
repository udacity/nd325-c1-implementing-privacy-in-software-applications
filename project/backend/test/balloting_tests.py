import pytest

import backend.main.api.balloting as balloting
import backend.main.api.registry as registry
from backend.main.objects.ballot import Ballot
from backend.main.objects.voter import Voter, VoterStatus, BallotStatus
from backend.main.store.data_registry import VotingStore

all_voters = [
    Voter("Adam", "Smith", "111111111"),
    Voter("Thien", "Huynh", "222222222"),
    Voter("Neel", "Banerjee", "333333333"),
    Voter("Linda", "Qi", "444444444"),
    Voter("Shoujit", "Gande", "555555555"),
]

class TestBalloting:
    def test_ballot_issuing(self):
        """
        Ensures that ballots can be issued to multiple voters.
        """
        for voter in all_voters:
            ballot_number = balloting.issue_ballot(voter)
            assert balloting.verify_ballot(voter, ballot_number)

    def test_multiple_ballot_issuing(self):
        """
        Ensures that multiple ballots can be issued to the same voter, and that they're all considered valid.
        """
        voter = all_voters[0]
        ballot_number1 = balloting.issue_ballot(voter)
        ballot_number2 = balloting.issue_ballot(voter)
        ballot_number3 = balloting.issue_ballot(voter)
        ballot_number4 = balloting.issue_ballot(voter)

        assert balloting.verify_ballot(voter, ballot_number1)
        assert balloting.verify_ballot(voter, ballot_number2)
        assert balloting.verify_ballot(voter, ballot_number3)
        assert balloting.verify_ballot(voter, ballot_number4)

    def test_count_ballot(self):
        """
        Ensures that ballots can be counted and tallied appropriately.
        """
        voter1, voter2, voter3 = all_voters[0:3]
        ballot_num1 = balloting.issue_ballot(voter1)
        ballot_num2 = balloting.issue_ballot(voter2)
        ballot_num3 = balloting.issue_ballot(voter3)

        all_candidates = registry.get_all_candidates()
        assert len(all_candidates) == 3

        ballot1 = Ballot(ballot_num1, all_candidates[0].candidate_id, "")
        ballot2 = Ballot(ballot_num2, all_candidates[1].candidate_id, "")
        ballot3 = Ballot(ballot_num3, all_candidates[1].candidate_id, "")

        assert balloting.count_ballot(ballot1, voter1) == BallotStatus.BALLOT_COUNTED
        assert balloting.count_ballot(ballot2, voter2) == BallotStatus.BALLOT_COUNTED
        assert balloting.count_ballot(ballot3, voter3) == BallotStatus.BALLOT_COUNTED

        assert registry.get_voter_status(voter1) == VoterStatus.BALLOT_COUNTED
        assert registry.get_voter_status(voter2) == VoterStatus.BALLOT_COUNTED
        assert registry.get_voter_status(voter3) == VoterStatus.BALLOT_COUNTED

        assert balloting.compute_election_winner().candidate_id == all_candidates[1].candidate_id

    def test_ballot_comment_redaction_composite(self):
        """
        Checks that comment redaction works
        """
        voter = all_voters[0]
        ballot_number = balloting.issue_ballot(voter)

        original_comment = """
        Hi there,
        My name is {0}, and prioritizing public transportation is _very_ important to me. It takes me at least 90
        minutes to get to work each day, largely because the infrastructure here hasn't been built yet. It's critical
        for us to invest in this. If you'd like to contact me please reach out to me at 329 112-4535, or at
        best_citizen@marsnet.co.mars.
        Cheers,

        {0} {1}
        Id: {2}
        """.format(voter.first_name, voter.last_name, voter.national_id).strip()

        all_candidates = registry.get_all_candidates()
        ballot = Ballot(ballot_number, all_candidates[0].candidate_id, original_comment)
        assert balloting.count_ballot(ballot, voter) == BallotStatus.BALLOT_COUNTED

        all_ballot_comments = balloting.get_all_ballot_comments()
        assert len(all_ballot_comments) == 1

        expected_redacted_comment = """
        Hi there,
        My name is {0}, and prioritizing public transportation is _very_ important to me. It takes me at least 90
        minutes to get to work each day, largely because the infrastructure here hasn't been built yet. It's critical
        for us to invest in this. If you'd like to contact me please reach out to me at [REDACTED PHONE NUMBER], or at
        [REDACTED EMAIL].

        Cheers,

        {0} {1}
        Id: {2}
        """.format("[REDACTED NAME]", "[REDACTED NAME]", "[REDACTED NATIONAL ID]").strip()
        assert list(all_ballot_comments)[0] == expected_redacted_comment

    def test_ballot_comment_redaction_phone_number(self):
        """
        Checks that comment redaction works
        """
        voter = all_voters[0]
        ballot_number = balloting.issue_ballot(voter)

        original_comment = """
        008 (839) 838-1627,008 839 838-1627,+8 839 838-1627,+8 839 838 1627,008 839 838 1627,0088398381627,(839) 838-1627,839-838-1627,8398381627""".strip()

        all_candidates = registry.get_all_candidates()
        ballot = Ballot(ballot_number, all_candidates[0].candidate_id, original_comment)
        assert balloting.count_ballot(ballot, voter) == BallotStatus.BALLOT_COUNTED

        all_ballot_comments = balloting.get_all_ballot_comments()
        assert len(all_ballot_comments) == 1

        expected_redacted_comment = """
        [REDACTED PHONE NUMBER],[REDACTED PHONE NUMBER],[REDACTED PHONE NUMBER],[REDACTED PHONE NUMBER],[REDACTED PHONE NUMBER],[REDACTED PHONE NUMBER],[REDACTED PHONE NUMBER],[REDACTED PHONE NUMBER],[REDACTED PHONE NUMBER]""".strip()
        assert list(all_ballot_comments)[0] == expected_redacted_comment

    def test_ballot_comment_redaction_national_id(self):
        """
        Checks that comment redaction works
        """
        voter = all_voters[0]
        ballot_number = balloting.issue_ballot(voter)

        original_comment = """
        345-23-2334
        345232334
        345 43 3452
        """.strip()

        all_candidates = registry.get_all_candidates()
        ballot = Ballot(ballot_number, all_candidates[0].candidate_id, original_comment)
        assert balloting.count_ballot(ballot, voter) == BallotStatus.BALLOT_COUNTED

        all_ballot_comments = balloting.get_all_ballot_comments()
        assert len(all_ballot_comments) == 1

        expected_redacted_comment = """
        [REDACTED NATIONAL ID]
        [REDACTED NATIONAL ID]
        [REDACTED NATIONAL ID]
        """.strip()
        assert list(all_ballot_comments)[0] == expected_redacted_comment

    def test_catch_fraud(self):
        """
        Checks to make sure that if someone is caught voting twice:

        1. Only their first ballot is counted
        2. The fraudster's name is recorded
        """
        voter = all_voters[0]
        ballot_number1 = balloting.issue_ballot(voter)
        ballot_number2 = balloting.issue_ballot(voter)
        ballot_number3 = balloting.issue_ballot(voter)

        all_candidates = registry.get_all_candidates()
        ballot1 = Ballot(ballot_number1, all_candidates[0].candidate_id, "first ballot")
        ballot2 = Ballot(ballot_number2, all_candidates[0].candidate_id, "second ballot")
        ballot3 = Ballot(ballot_number3, all_candidates[0].candidate_id, "third ballot")

        # Have the voter commit fraud
        assert balloting.count_ballot(ballot1, voter) == BallotStatus.BALLOT_COUNTED
        assert balloting.count_ballot(ballot2, voter) == BallotStatus.FRAUD_COMMITTED
        assert registry.get_voter_status(voter) == VoterStatus.FRAUD_COMMITTED
        assert balloting.count_ballot(ballot3, voter) == BallotStatus.FRAUD_COMMITTED
        assert registry.get_voter_status(voter) == VoterStatus.FRAUD_COMMITTED

        # Make sure the fraudster's name is recorded
        fraudsters = balloting.get_all_fraudulent_voters()
        assert len(fraudsters) == 1
        assert (voter.first_name + " " + voter.last_name) in balloting.get_all_fraudulent_voters()

        # Make sure ballot 2 and 3 weren't counted
        ballot_comments = balloting.get_all_ballot_comments()
        assert len(ballot_comments) == 1
        assert "first ballot" in ballot_comments

    def test_de_register_fraudster(self):
        """
        Checks that fraudsters cannot be completely de-registered
        """
        voter = all_voters[0]
        ballot_number1 = balloting.issue_ballot(voter)
        ballot_number2 = balloting.issue_ballot(voter)

        all_candidates = registry.get_all_candidates()
        ballot1 = Ballot(ballot_number1, all_candidates[0].candidate_id, "first ballot")
        ballot2 = Ballot(ballot_number2, all_candidates[0].candidate_id, "second ballot")

        # Commit Fraud
        assert balloting.count_ballot(ballot1, voter) == BallotStatus.BALLOT_COUNTED
        assert balloting.count_ballot(ballot2, voter) == BallotStatus.FRAUD_COMMITTED

        # De-register the voter
        assert registry.de_register_voter(voter) is False

        # Make sure the fraudster's name is still recorded
        fraudsters = balloting.get_all_fraudulent_voters()
        assert len(fraudsters) == 1
        assert (voter.first_name + " " + voter.last_name) in balloting.get_all_fraudulent_voters()

        # Make sure the voter's status is still that fraud was committed
        assert registry.get_voter_status(voter) == VoterStatus.FRAUD_COMMITTED

    def test_invalidate_ballot_before_use(self):
        """
        Ensures that an invalidated ballot cannot be used
        """
        voter = all_voters[0]
        ballot_number1 = balloting.issue_ballot(voter)

        all_candidates = registry.get_all_candidates()
        ballot1 = Ballot(ballot_number1, all_candidates[0].candidate_id, "")

        assert balloting.invalidate_ballot(ballot_number1)
        assert balloting.count_ballot(ballot1, voter) == BallotStatus.INVALID_BALLOT

        # However, ensure the voter can still vote with another ballot
        ballot_number2 = balloting.issue_ballot(voter)
        ballot2 = Ballot(ballot_number2, all_candidates[0].candidate_id, "")

        assert balloting.count_ballot(ballot2, voter) == BallotStatus.BALLOT_COUNTED

    def test_invalidate_ballot_after_use(self):
        """
        Ensures that a ballot that is cast cannot be invalidated
        """
        voter = all_voters[0]
        ballot_number1 = balloting.issue_ballot(voter)

        all_candidates = registry.get_all_candidates()
        ballot1 = Ballot(ballot_number1, all_candidates[0].candidate_id, "valid now, but invalid later")

        assert balloting.count_ballot(ballot1, voter) == BallotStatus.BALLOT_COUNTED
        assert balloting.invalidate_ballot(ballot_number1) is False

        # The ballot cannot be invalidated after being cast - it should still be counted
        assert len(balloting.get_all_ballot_comments()) == 1

    def test_count_ballot_mismatch(self):
        """
        If the wrong voter issues a ballot, the count_ballot endpoint should say so. The ballot should still remain
        for the true voter to used
        """
        voter1, voter2 = all_voters[0:2]
        ballot_number2 = balloting.issue_ballot(voter2)

        all_candidates = registry.get_all_candidates()

        # Have the wrong voter cast the ballot
        ballot2_attempt1 = Ballot(ballot_number2, all_candidates[0].candidate_id, "Attempt 1")
        assert balloting.count_ballot(ballot2_attempt1, voter1) == BallotStatus.VOTER_BALLOT_MISMATCH

        # Now, have the right voter cast the ballot
        ballot2_attempt2 = Ballot(ballot_number2, all_candidates[1].candidate_id, "Attempt 2")
        assert balloting.count_ballot(ballot2_attempt2, voter2) == BallotStatus.BALLOT_COUNTED

        ballot_comments = balloting.get_all_ballot_comments()
        assert len(ballot_comments) == 1
        assert "Attempt 2" in ballot_comments

    def test_issue_ballot_unregistered_voter(self):
        """
        Checks that you cannot issue a ballot to an unregistered voter
        """
        unregistered_voter = Voter("Daniel", "Salt", "999-99-9999")
        assert balloting.issue_ballot(unregistered_voter) is None

    def test_unregistered_voter_count_ballot(self):
        """
        Checks that an unregistered voter cannot use an existing ballot for another voter to vote.
        """
        unregistered_voter = Voter("Daniel", "Salt", "999-99-9999")
        registered_voter = all_voters[0]
        valid_ballot_number = balloting.issue_ballot(registered_voter)

        all_candidates = registry.get_all_candidates()

        valid_ballot = Ballot(valid_ballot_number, all_candidates[0].candidate_id, "Valid Ballot")
        assert balloting.count_ballot(valid_ballot, unregistered_voter) == BallotStatus.VOTER_BALLOT_MISMATCH

    def test_count_election_winner_plurality(self):
        """
        If nobody gets the majority, the winner still is the one with the plurality.
        """
        all_candidates = registry.get_all_candidates()

        voter1, voter2, voter3, voter4 = all_voters[0:4]
        ballot_number1 = balloting.issue_ballot(voter1)
        ballot_number2 = balloting.issue_ballot(voter2)
        ballot_number3 = balloting.issue_ballot(voter3)
        ballot_number4 = balloting.issue_ballot(voter4)

        # No candidate has a majority, but one has a plurality.
        ballot1 = Ballot(ballot_number1, all_candidates[0].candidate_id, "")
        ballot2 = Ballot(ballot_number2, all_candidates[0].candidate_id, "")
        ballot3 = Ballot(ballot_number3, all_candidates[1].candidate_id, "")
        ballot4 = Ballot(ballot_number4, all_candidates[2].candidate_id, "")

        balloting.count_ballot(ballot1, voter1)
        balloting.count_ballot(ballot2, voter2)
        balloting.count_ballot(ballot3, voter3)
        balloting.count_ballot(ballot4, voter4)

        assert balloting.compute_election_winner() == all_candidates[0]

    @pytest.fixture(autouse=True)
    def run_around_tests(self):
        """
        Sets up the candidates and voters
        """
        VotingStore.refresh_instance()

        # Populate candidates
        expected_candidate_names = {"Kathryn Collins", "Aditya Guha", "Rina Harvey"}
        for candidate_name in expected_candidate_names:
            registry.register_candidate(candidate_name)

        # Populate voters
        for voter in all_voters:
            registry.register_voter(voter), "Couldn't register {0} {1}".format(
                voter.first_name, voter.last_name)

        yield
