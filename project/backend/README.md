## Privacy Engineering Project 1 - Project Instructions


#### Introduction

After many years of deep civil unrest among disputing factions of human colonists of Mars, finally, a peace deal has been struck and the Republic of Mars has been formed. When creating the republic, the colonists have agreed to hold elections to choose their leader, the Chancellor of the Republic of Mars (COTREM), every 5 years, by simple popular vote.

The first set of elections is to take place soon, and while peace has been found, it might not last if the election process is disputed, or controversial. To alleviate the public concern, the founding delegation of the Republic of Mars has nominated you, an expert in privacy engineering, to build out a reliable, and privacy-protective voting system.


#### Completion Requirements

In order to successfully complete this project, you’ll have to:

Pass all the series of checks provided in the project. These tests ensure that you haven’t broken anything during your implementation, and serve to verify that certain functional and privacy features have been implemented.
Submit your implementations of certain Python files (ballot.py and voter.py). These will be reviewed by our reviewers.
Fill out a final self-evaluation of the software you have built, and submit it to our reviewers for grading. This helps us check your understanding of some of the privacy features of the application you’ve just built.

Remember that privacy and security are related concepts, and are both important. However, while security generally deals with outsider threats, and preventing them from exploiting the system for their gain, privacy has to do with minimizing compromising information that could be nefariously extracted, even by an inside actor. While security is important for this project, our main focus here is privacy engineering.


#### Step 1: Get the Code

You can access the code in <THIS GITHUB> link, or in the Udacity workspace.



#### Step 2: Explore the Codebase

We’ve started you off with some starter code -- have a look at what we’ve provided up to this point.

Specifically, a few files to look at are:

```
backend/objects/voter.py
backend/objects/candidate.py
backend/objects/ballot.py
```

Should you feel the need to, you are more than welcome to make additive changes to the classes in these files. However, please do not remove classes or fields in those classes that already exist.

We’d also recommend having a look at:

```
backend/api/registry.py
```

... as well as the files in the `backend/store/` package. We'd like to call special attention to the `backend/store/secret_registry.py` file - if you need to generate secrets, such as salts, peppers or encryption/decryption keys, please use this file to do so. Feel free to add more methods here, but we’d recommend following the general pattern that we’ve established.

#### Step 3: Build out the Voter class

If you open up the `backend/objects/voter.py`, you’ll see that we have pre-made a `SensitiveVoter` class, and an `ObfuscatedVoter` class. The reason we’re doing this is so that we only use the `SensitiveVoter` class when it’s necessary -- in all other places, we use the `ObfuscatedVoter` class.

You’ll notice that the `SensitiveVoter` class has a national_id field. We consider this to be a sensitive field, much like Social Security Numbers (SSNs) are sensitive in the United States.

Your job in this step is to determine a privacy-protecting scheme to populate the `ObfuscatedVoter` class. Do this in `SensitiveVoter.get_obfuscated_voter`. Feel free to use other parts of the starter code to bolster your implementation.


#### Step 4: Build out our Ballot Class

Our next task is to build out our conception of a ballot, specifically, the way we assign and label ballots. There are a couple important considerations when designing ballot tracking.

1. Voters can be issued multiple ballots. This can be because a voter might make a mistake when filling out one ballot, and therefore might need an additional ballot. However it's important that only one ballot per voter is counted.
2. All ballots must be secret. Voters have the right to cast secret ballots, which means that it should be technically impossible for someone holding a filled-out ballot to associate that ballot with the voter. 
3. In order to minimize the risk of fraud, a nefarious actor should not be able to tell that different two ballots are associated with the same voter.

The unique identifier for a ballot is a `BallotNumber` and is defined in `backend/objects/ballot.py`. In this section, your job is to define a scheme produce a new ballot number. In the `backend/objects/ballot.py` file, implement the `generate_ballot_number` method. Currently this method takes nothing as input, but feel free to add inputs as you feel are appropriate.

#### Step 5: Sensitive Data Detection

As you might have seen in the `Ballot` class in `ballot.py`, voters have the right to add a free-text comment when casting their ballot. This comment has no impact on the election, but rather serves to allow voters to voice their concerns in a more nuanced manner. However, this right of public comment could easily undermine the secret ballot.

In this section, your job is to find a way to redact personally identifiable information from a specific public comment. In particular, we care about the following:

1. The voter's name (first and/or last)
2. The voter's phone number
3. The voter's National Identifier
4. The voter's email address

Phone numbers can take various formats. Here are some examples of valid phone numbers:

1. `008 (299) 483-2343`
2. `008 299 483-2343`
3. `+8 299 483-2343`
3. `+8 299 483 2343`
4. `008 299 483 2343`
5. `0082994832343`
6. `(299) 483-2343`
7. `299-483-2343`
8. `2994832343`

National Identifiers only have a few formats:

1. `345-23-2334`
2. `345232334`
3. `345 43 3452`

For each type of PII, we want to redact only that specific bit of information, but provide the context as to what that information was (i.e. a national identifier, a phone number, or a name) For example, if someone were to write the comment:

```
I'm so proud to be voting for the first time ever! If there are any problems with my vote please reach out to me at (345) 553-2335.
I'm also available over email at sjenkins@email.co.mars.

Best,

Sara Jenkins
ID: 234-23-2342
```

This should be redacted to:

```
I'm so proud to be voting for the first time ever! If there are any problems with my vote please reach out to me at [REDACTED PHONE NUMBER].
I'm also available over email at [REDACTED EMAIL].


Best,

[REDACTED NAME] [REDACTED_NAME]
ID: [REDACTED NATIONAL ID]
```


Do note that candidate names are not considered to be sensitive, as candidates themselves must be public figures, and their names are on the ballot already.

Please implement the `redact_free_text` method in the `backend/detection/pii_detection.py` file. Feel free to add additional arguments to the method here.


#### Step 6: Registry API

If you look into `backend/api/setup_api.py`, you'll see that there are methods for registering voters and getting information about voter registration. Your next task is to finish these methods.

Specifically, we're referring to:

1. `register_voter`
2. `get_voter_status`
3. `de_register_voter` - note: fraudulent voters can be de-registered, but their fraudulent status should still be reflected

We've also completed methods for adding candidates into the database. Have a look at `register_candidate` and `is_candidate_registered`. These are completed methods that you do not have to modify (unless you really want to). These can serve as your example.
In particular, it's worthwhile having a look into the `VotingStore` class in `backend/store/data_registry.py`, which encapsulates the database. Here, you'll find a `create_tables` method, where you should feel free to add in whatever tables you'll need to store data into.
Feel free to pattern match against our example for the candidate registration process.

Please do NOT change the inputs or outputs to any of the methods in this class - we use these methods for running our unit tests against your code.


#### Step 7: Balloting API

Now that we have a decent chunk of the privacy features ready, let's actually get to the meat of the application we're trying to build - vote counting. As you know, a system that does nothing of value can trivially be made to be privacy protective.

In the `backend/api/balloting.py` file, please implement the following APIs:

1. `issue_ballot`
2. `count_ballot`
3. `get_fraud_list`
4. `invalidate_ballot`
5. `verify_ballot`
6. `get_all_ballot_comments`
7. `compute_election_winner`

Remember, it's important that when implementing `count_ballot`, that you only count _one_ ballot per voter. Additionally, if a voter attempts to count more than once, only their first vote should be counted, but they should be flagged as having committed fraud. Additionally, remember to include the redaction of the ballot comment that you implemented in a previous step. 

Also recall that the `VotingStore` class in `backend/store/data_registry.py`, which encapsulates the database, might have to be extended, like you did in the previous step.


#### Step 8: Frontend Changes

At this point, our backend is fully built out. Now, we need to make some changes to our frontend.

There are some basic things we want to communicate to the user.

1. Before the voter casts their ballot, the frontend should communicate that after verifying their identity, their vote will be counted _anonymously_.
2. After the ballot has been cast, the voter should be informed that their ballot has been submitted that the submission was successful.
3. After the voter has voted, the voter should be informed that they're free to de-register themselves from voting, if they contact the voter registrar.
