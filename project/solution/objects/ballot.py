
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
    def __init__(self, ballot_number: BallotNumber):
        # TODO: Implement this
        self.ballot_number = ballot_number
        raise NotImplementedError()


