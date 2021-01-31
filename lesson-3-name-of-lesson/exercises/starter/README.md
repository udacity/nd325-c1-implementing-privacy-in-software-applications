# Lesson 3: Tracking Sensitive Data

### Exercise 3: Regex Practice

Let's try to write some code to find _and remove_ cell phone numbers from some free text inputs.

To do this, we'll have to implement the `redact_phone_numbers` method in the `pii_detection.py` file. In this method,
construct a regex that matches phone numbers of the following formats:

1. `(299) 483-2343`
2. `299 483-2343`
3. `299-483-2343`
4. `2994832343`

Feel free to search online for a regex, and test it on a regex testing site like [regex101](https://regex101.com/) or
[regex planet](https://www.regexplanet.com/advanced/python/index.html).

Have the phone numbers be replaced by the text `[REDACTED PHONE NUMBER]`.

When you're done, you can run the tests by running `pytest test_regex_redaction.py` from the `test/` directory. All 
these tests should pass.

Be sure to NOT modify the method signature, for this to work.


### Exercise 4: Overlap Practice

Let's try to write some code to find _and remove_ ID numbers from some free text inputs.

To do this, we'll have to implement the `redact_id_numbers` method in the `pii_detection.py` file. We've provided you
a method called `create_id_numbers_set` in the same file that produces a massive list of ID numbers. Most of these
follow a pattern, but a few of these are totally random (this is sometimes the case when dealing with legacy data).

Use this list to perform overlap detection of these ID numbers, and replace all ID numbers that you find with the text
`[REDACTED ID NUMBER]`.

When you're done, you can run the tests by running `pytest test_overlap_redaction.py` from the `test/` directory. All 
these tests should pass.

Be sure to NOT modify the method signature, for this to work.
