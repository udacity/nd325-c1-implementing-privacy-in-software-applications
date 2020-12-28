#
# This file is the REST API for our frontend to get data from.
#
# To run the backend server locally, please run the following from the /backend directory
#
# $ export FLASK_APP=api/backend_rest_api.py
# $ flask run
#

from flask import Flask, request
import backend.api.balloting as balloting
import backend.api.registry as registry
from backend.objects.voter import SensitiveVoter
from backend.objects.ballot import Ballot
import jsons
from flask_cors import CORS

app = Flask(__name__)
CORS(app, resources={r"/api/*": {"origins": "http://localhost:3000"}})


@app.route('/')
def ping():
    return 'pong'


@app.route('/api/count_ballot', methods=["POST"])
def count_ballot():
    req_data = request.get_json()
    ballot_number = req_data['ballot_number']
    chosen_candidate_id = req_data['chosen_candidate_id']
    voter_comments = req_data['voter_comments']
    voter = SensitiveVoter(req_data['voter_national_id'])

    ballot = Ballot(ballot_number, chosen_candidate_id, voter_comments)
    return jsons.dumps(balloting.count_ballot(ballot, voter))


@app.route('/api/verify_ballot', methods=["POST"])
def verify_ballot():
    req_data = request.get_json()
    ballot_number = req_data['ballot_number']
    voter = SensitiveVoter(req_data['voter_national_id'])
    return jsons.dumps(balloting.verify_ballot(voter, ballot_number))


@app.route('/api/get_all_candidates')
def get_all_candidates():
    return jsons.dumps(registry.get_all_candidates())


def populate_database():
    """
    This method is for you as a developer. This is where you can add more candidates for the election,
    register voters for the election and issue ballots. This method is strictly for your convenience, and
    is not part of the rubric for the final project.
    """

    # Adding Candidates for the election. These should be reflected in the frontend.
    registry.register_candidate("Bob Jenkins")
    registry.register_candidate("Alice Johnson")
    registry.register_candidate("Jim Kirk")

    # TODO: Feel free to add voters to the voter registry, and issue ballots


populate_database()
