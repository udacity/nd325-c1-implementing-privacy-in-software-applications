#
# DO NOT MODIFY THIS FILE
#


from flask import Flask, request
from werkzeug.exceptions import HTTPException
import solution.api.balloting as balloting
import solution.api.initialize as initialization
from solution.objects.voter import SensitiveVoter
from solution.objects.ballot import Ballot
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
    return jsons.dumps(initialization.get_all_candidates())


# @app.errorhandler(NotImplementedError)
# def handle_not_implemented_error(e):
#     return jsons.dumps({
#         "data": {
#             "code": 500,
#             "name": "Not Implemented",
#             "description": "This endpoint has not yet been implemented",
#         },
#         "content_type": "application/json"
#     })

#
# @app.errorhandler(HTTPException)
# def handle_exception(e):
#     """Return JSON instead of HTML for HTTP errors."""
#     # start with the correct headers and status code from the error
#     response = e.get_response()
#     # replace the body with JSON
#     response.data = jsons.dumps({
#         "code": e.code,
#         "name": e.name,
#         "description": e.description,
#     })
#     response.content_type = "application/json"
#     print(jsons.dumps(response))
#
#     return response


def populate_database():
    initialization.register_candidate("Bob Jenkins")
    initialization.register_candidate("Alice Johnson")
    initialization.register_candidate("Jim Kirk")


populate_database()
