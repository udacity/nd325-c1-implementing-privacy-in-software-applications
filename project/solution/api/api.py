#
# DO NOT MODIFY THIS FILE
#


from flask import Flask
import solution.api.balloting as balloting
import solution.api.initialize as initialization
from solution.objects.voter import SensitiveVoter
from solution.objects.ballot import Ballot, BallotNumber
from solution.objects.candidate import Candidate
import jsons

app = Flask(__name__)


@app.route('/')
def ping():
    return 'pong'


@app.route('/api/count_ballot', methods=["POST"])
def count_ballot(ballot_number: BallotNumber, candidate: Candidate, voter_comments: str, voter: SensitiveVoter):
    ballot = Ballot(ballot_number, candidate, voter_comments)
    return jsons.dumps(balloting.count_ballot(ballot, voter))


@app.route('/api/verify_ballot')
def verify_ballot(voter: SensitiveVoter, ballot_number: BallotNumber):
    return jsons.dumps(balloting.verify_ballot(voter, ballot_number))


@app.route('/api/get_all_candidates')
def get_all_candidates():
    return jsons.dumps(initialization.get_all_candidates())


def execute():
    initialization.register_candidate("Bob Jenkins")
    initialization.register_candidate("Alice Johnson")
    initialization.register_candidate("Sudip Guha")


execute()
