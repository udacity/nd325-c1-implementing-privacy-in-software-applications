
from solution.objects.candidate import Candidate

class BallotNumber:
    """
    A class that wraps a ballot number
    """
    def __init__(self, ballot_number: str):
        self.ballot_number = ballot_number


class Ballot:
    """
    A ballot that exists in a specific, secret manner
    """
    def __init__(self, ballot_number: BallotNumber, candidate_chosen: Candidate, voter_comments: str):
        # TODO: Implement this
        self.ballot_number = ballot_number
        self.candidate_chosen = candidate_chosen
        self.voter_comments = voter_comments
        raise NotImplementedError()
