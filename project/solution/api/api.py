#
# DO NOT MODIFY THIS FILE
#


from flask import Flask
from typing import List
import solution.api.balloting as balloting
import solution.api.initialize as initialization
from solution.objects.voter import SensitiveVoter
from solution.objects.ballot import Ballot, BallotNumber
from solution.objects.candidate import Candidate

app = Flask(__name__)


@app.route('/')
def ping():
    return 'pong'


@app.route('/api/count_ballot')
def count_ballot(ballot_number: BallotNumber, candidate: Candidate, voter_comments: str, voter: SensitiveVoter) -> bool:
    ballot = Ballot(ballot_number, candidate, voter_comments)
    return balloting.count_ballot(ballot, voter)


@app.route('/api/verify_ballot')
def verify_ballot(voter: SensitiveVoter, ballot_number: BallotNumber):
    return balloting.verify_ballot(voter, ballot_number)


@app.route('/api/get_all_candidates')
def get_all_candidates() -> List[Candidate]:
    return initialization.get_all_candidates()


if __name__ == "__main__":
    # TODO(mpatil): populate the store with candidates
    pass