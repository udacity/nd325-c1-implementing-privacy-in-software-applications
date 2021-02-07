# Lesson 4 Exercises


### Exercise 1: Hashing with a Pepper

Let's suppose you're working with your local unemployment benefit office, and your job is to make an application that
stores a collection of national identifiers (i.e. Social Security Numbers) for those who are unemployed, so they can
receive unemployment benefits.

In your nation or state, people who are unemployed apply for unemployment benefits. However, their application is only
approved if they are in the unemployment registry.

Being a privacy engineer, your know that to accomplish this, there is no reason that anyone ever has to see the full set
of all unemployed people's national identifiers. In fact, there's no reason to even store copies of the SSN -- you can
simply hash them and compare the hashes.

Implement hashing with a pepper for SSNs in this exercise. In the `src/main/unemployment/privacy.py` file,
there's a `obfuscated_national_id` method. Implement this. Feel free to generate and register your secrets (if
necessary) in `secret_registry.py`.


### Exercise 2: Deterministic Encryption 

We soon realized that we also needed to store email addresses into this store. This allows the unemployment department to
reach out to beneficiaries with important communications, and perhaps job opportunities.

Because of this, we need the ability to get _all_ the email addresses from the system.

In the `src/main/unemployment/unemployment_api.py` file, there's a `get_all_email_addresses` method that is already
implemented. This method relies on the `encrypt_email_address` and `decrypt_email_address` that are in the
`src/main/unemployment/privacy.py` file. Implement these. Feel free to generate and register your secrets (if necessary)
in `secret_registry.py`.


### Exercise 3: Non-deterministic encryption 

While we want to enable the workflow to check if a given known individual is in prison, but not the workflow that allows
someone to see _all_ the unemployed individuals who are also in prison (unless they painstakingly look through the
whole database).

However, whether or not a person is incarcerated has only two possible values: true or false. Therefore we must employ a
non-deterministic encryption strategy. 

This requires implementing on the `encrypt_incarceration_status` and `decrypt_incarceration_status` that are in the
`src/main/unemployment/privacy.py` file. Feel free to generate and register your secrets (if necessary) in
`secret_registry.py`.