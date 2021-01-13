## Privacy Engineering Project 1 - Project Instructions


### Introduction

After many years of deep civil unrest among disputing factions of colonists of Atlantis, finally, a peace deal has
been struck and the Republic of Atlantis has been formed. When creating the republic, the colonists have agreed to hold
elections to choose their leader, the Chancellor of the Republic of Atlantis (COTREA), every 5 years, by simple popular
vote.

The first set of elections is to take place soon, and while peace has been found, it might not last if the election
process is disputed, or controversial. To alleviate the public concern, the founding delegation of the Republic of
Atlantis has nominated you, an expert in privacy engineering, to build out a reliable, and privacy-protective voting
system.


### Completion Requirements

In order to successfully complete this project, you’ll have to:

1. **Pass all the checks provided in the project.** These tests ensure that you haven’t broken anything during your
   implementation, and serve to verify that certain functional and privacy features have been implemented.
   1. You can run these tests from the `backend/` directory by running `$ pytest`.
2. **Submit your implementations of certain Python files.** These will be reviewed by our reviewers. 
   1. `ballot.py`
   2. `voter.py`
3. **Submit screenshots of the frontend**. These will be reviewed by our reviewers.
   1. A screenshot of the frontend before anything has been filled in.
   2. A screenshot of the frontend after a vote has successfully been cast.
4. Fill out a final self-evaluation of the software you have built, and submit it to our reviewers for grading. This
   helps us check your understanding of some of the privacy features of the application you’ve just built.

Remember that privacy and security are related concepts, and are both important. However, while security generally deals
with outsider threats, and preventing them from exploiting the system for their gain, privacy has to do with minimizing
compromising information that could be nefariously extracted or used, even by an inside actor. While security is
important for this project, our main focus here is privacy engineering.

### Prerequisites

On your virtual machine, please install the following packages

1. Python3 Packages - `flask`, `jsons`, `flask-CORS`, `Flask-API` and `pytest`.
   Also recommended are `bcrypt` and `pycryptodome`. All these can be found in `backend/requirements.txt`. You can
   install these by running `$ pip install -r requirements.txt` from the `backend/` directory.
2. Node Package Manager (NPM) packages - `typescript`, `react`, `react-dom`, `@blueprintjs/core`, `@blueprintjs/icons`


### Running Unit Tests

We have provided unit tests for this project in the `backend/test/` directory. You can run _all_ these by running:

```
$ cd backend/
$ pytest
```

You can also run individual test files by specifying their paths, like so:

```
$ cd backend
$ pytest test/registry_tests.py
```

What each test checks for is outline in the method documentation for each testing method.

### Project Guide

#### Step 1: Get the Code

You can access the code [here](https://github.com/udacity/nd325-c1-implementing-privacy-in-software-applications), or in
the Udacity workspace.


#### Step 2A: Explore the Codebase

We’ve started you off with some starter code -- have a look at what we’ve provided up to this point.

Specifically, a few files to look at are:

```
backend/main/objects/voter.py
backend/main/objects/candidate.py
backend/main/objects/ballot.py
```

... as well as the files in the `backend/main/store/` package. We'd like to call special attention to the
`backend/main/store/secret_registry.py` file - if you need to generate secrets, such as salts, peppers or
encryption/decryption keys, please use this file to do so. Feel free to add more methods here, but we’d recommend
following the general pattern that we’ve established.


#### Step 2B: Run the Frontend & Backend

To run the frontend locally, run the following:

```
$ cd frontend
$ npm start  # This should open the frontend in your browser
```

To run the backend locally, do the following:

```
$ cd backend/
$ export FLASK_APP=main/api/backend_rest_api.py  # only need to do that once
$ flask run
```

Note that it is important to run the frontend and backend together (so you'll probably need multiple command line
windows).

Give the frontend a whirl - it should error when you try to submit a ballot, but that's only because you haven't built
the backend yet. The candidates that you see in the frontend are actually populated in from the `populate_database`
method in `backend/main/api/backend_rest_api.py`. Feel free to modify this method as you implement more functionality
in this project.

#### Step 3: Build out the Voter class

If you open up the `backend/main/objects/voter.py`, you’ll see that we have pre-made a `Voter` class, and a
`MinimalVoter` class. The reason we’re doing this is so that we only use the `Voter` class when it’s necessary -- in all
other places, we use the `MinimalVoter` class.

You’ll notice that the `Voter` class has a `national_id` field. We consider this to be a sensitive field, much like
Social Security Numbers (SSNs) are sensitive in the United States.

Your job in this step is to determine a privacy-protecting scheme to populate the `MinimalVoter` class. You can see
we've provided you the `Voter.get_minimal_voter` function, that calls `obfuscated_national_id` and `encrypt_name`
functions. Feel free to use other parts of the starter code to bolster your implementation.

When you implement `encrypt_name`, you might also want to implement `decrypt_name`, as this will be useful later when
you have to find the names of fraudsters. Remember that because these are names, and there are some names that are
fairly common, we want this encryption to be a non-deterministic encryption.

#### Step 4: Build out our Ballot Class

Our next task is to build out our conception of a ballot, specifically, the way we assign and label ballots.
There are a couple important considerations when designing ballot tracking.

1. **Voters can be issued multiple ballots.** This can be because a voter might make a mistake when filling out one
   ballot, and therefore might need an additional ballot. However it's important that only one ballot per voter is
   counted.
2. **All ballots must be secret.** Voters have the right to cast secret ballots, which means that it should be
   technically impossible for someone holding a ballot to associate that ballot with the voter. 
3. In order to minimize the risk of fraud, a nefarious actor should not be able to tell that two different ballots are
   associated with the same voter.

The unique identifier for a ballot is a string that we call a `ballot_number` and is defined in the `Ballot` class in 
`backend/main/objects/ballot.py`. In this section, your job is to define a scheme to produce a new ballot number; in the
`backend/main/objects/ballot.py` file, implement the `generate_ballot_number` method. Currently this method takes
nothing as input, but feel free to add inputs as you feel are appropriate.

#### Step 5: Sensitive Data Detection

As you might have seen in the `Ballot` class in `ballot.py`, voters have the right to add a free-text comment when
casting their ballot. This comment has no impact on the election, but rather serves to allow voters to voice their
concerns in a more nuanced manner. However, this right of public comment could easily undermine the secrecy of the
ballot.

In this section, your job is to find a way to redact personally identifiable information (PII) from a public comment.
In particular, we care about the following:

1. The voter's name (first and/or last)
2. The voter's phone number
3. The voter's National Identifier
4. The voter's email address

Phone numbers can take various formats. Here are some examples of valid phone numbers:

1. `(299) 483-2343`
2. `299 483-2343`
3. `299-483-2343`
4. `2994832343`

National Identifiers also have multiple formats:

1. `345-23-2334`
2. `345232334`
3. `345 43 3452`

For each type of PII, we want to redact only that specific bit of information, but provide the context as to what that
information was (i.e. a national identifier, a phone number, or a name) For example, if someone were to write the
comment:

```
I'm so proud to be voting for the first time ever! If there are any problems with my vote please reach out to me at
(345) 553-2335. I'm also available over email at sjenkins@email.co.atlantis.

Best,

Sara Jenkins
ID: 234-23-2342
```

This should be redacted to:

```
I'm so proud to be voting for the first time ever! If there are any problems with my vote please reach out to me at
[REDACTED PHONE NUMBER]. I'm also available over email at [REDACTED EMAIL].


Best,

[REDACTED NAME] [REDACTED_NAME]
ID: [REDACTED NATIONAL ID]
```

Do note that candidate names are not considered to be sensitive, as candidates themselves must be public figures, and
their names are on the ballot already.

Please implement the `redact_free_text` method in the `backend/main/detection/pii_detection.py` file. Feel free to add
additional arguments to the method here.

#### Step 6: Registry API

If you look into `backend/main/api/registry.py`, you'll see that there are methods for registering voters and getting
information about voter registration. Your next task is to finish these methods.

Specifically, we're referring to:

1. `register_voter`
2. `get_voter_status`
3. `de_register_voter` - note: fraudulent voters cannot be de-registered

The method documentation on these methods in the starter code should give you a sufficient idea of how to implement
these.

We've also completed methods for adding candidates into the database. Have a look at `register_candidate` and
`is_candidate_registered`. These are _completed_ methods that you do NOT have to modify (unless you really want to).
These can serve as your example. In particular, it's worthwhile having a look at the `VotingStore` class in
`backend/main/store/data_registry.py`, which encapsulates the database. Here, you'll find a `create_tables` method,
where you should feel free to add in whatever tables you'll need to store data into. Feel free to pattern match against
our example for the candidate registration process.

Please do NOT change the inputs or outputs to any of the methods in the `registry.py` file - we use these methods for
running our unit tests against your code.

After this step, all the unit tests in `backend/test/registry_tests.py` should pass.

#### Step 7: Balloting API

Now that we have a decent chunk of the privacy features ready, let's actually get to the meat of the application we're
trying to build - vote counting.

In the `backend/main/api/balloting.py` file, please implement the following APIs. The method documentation in the code
should give you an idea as to what each is meant to do. Additionally, you may have to use methods from previous parts of
this project to accomplish the full feature set here.

1. `issue_ballot`
2. `count_ballot`
3. `get_fraud_list`
4. `invalidate_ballot`
5. `verify_ballot`
6. `get_all_ballot_comments`
7. `compute_election_winner`
8. `get_all_fraudulent_voters`

Remember, it's important that when implementing `count_ballot`, that you only count _one_ ballot per voter.
Additionally, if a voter attempts to count more than once, only their first vote should be counted, but they should be
flagged as having committed fraud. Remember to include the redaction of the ballot comment that you implemented in a
previous step. 

Also recall that the `VotingStore` class in `backend/main/store/data_registry.py`, which encapsulates the database,
might have to be extended, like you did in the previous step.

And again, please do NOT change the inputs or outputs to any of the methods in the `balloting.py` file - we use these
methods for running our unit tests against your code.

After this step, all the unit tests in `backend/test/balloting_tests.py` and `backend/test/privacy_sanity_tests.py`
should pass.

#### Step 8: Frontend Changes

At this point, our backend is fully built out. Now, we need to make some changes to our frontend.

There are some basic things we want to communicate to the user. You'll want to make these changes in
`frontend/src/ballotForm.tsx`.

1. Before the voter casts their ballot, the frontend should communicate that, after verifying their identity, their vote
   will be counted _anonymously_.
2. Before the voter casts their ballot, the frontend should ask them to not put any information identifying themselves
   or others in the "comments" section of the ballot.
   1. While we do check for PII, it's safest if the voter is informed of the risk beforehand
3. After the ballot has been cast, the voter should be informed that their ballot has been submitted and that the
   submission was successful.
4. After the voter has voted, the voter should be informed that they're free to de-register themselves from voting, if
   they contact the voter registrar.
   
After completing this, please take two screenshots of your frontend:

1. One before anything has been filled in (call it `zero_state.png`)
2. One immediately after a ballot has been successfully submitted (call it `after_voting.png`)

Add these files to the `submission/` directory in this repository.

#### Step 9: Privacy Self-Evaluation

Congratulations! You've finished the technical portion of the project. At this time, it's important for us to have a
look back at what we've built from a privacy angle.

For each of the seven Privacy by Design (PbD) principle, go through an answer the following two questions:

1. What does this application do to address this PbD principle?
2. How can we improve this application to better address this PbD principle?

Please do this in the `submission/pbd-self-evaluation.txt` file that we've provided.


### Acknowledgements

This project was made using technology from the following sources:

1. Frontend: [Blueprint](https://blueprintjs.com/docs/), [Typescript](https://www.typescriptlang.org/),
   [React](https://reactjs.org/) and [NPM](https://www.npmjs.com/)
2. Backend: [Flask](https://flask.palletsprojects.com/en/1.1.x/), [Python 3](https://www.python.org/),
   [Jsons](https://github.com/ramonhagenaars/jsons), [Flask-CORS](https://flask-cors.readthedocs.io/en/latest/),
   [Flask-API](https://www.flaskapi.org/), [Pytest](https://docs.pytest.org/en/stable/),
   [brcrypt](https://pypi.org/project/bcrypt/) and
   [pycryptodome](https://pycryptodome.readthedocs.io/en/latest/src/introduction.html)
   
