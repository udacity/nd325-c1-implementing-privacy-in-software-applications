class Ballot:
    """
    A ballot that exists in a specific, secret manner
    """
    def __init__(self, ballot_number: str, chosen_candidate_id: str, voter_comments: str):
        self.ballot_number = ballot_number
        self.chosen_candidate_id = chosen_candidate_id
        self.voter_comments = voter_comments
        raise NotImplementedError()


def generate_ballot_number():
    # TODO: Implement this! Feel free to add parameters to this method, if necessary
    raise NotImplementedError()
