
**Open Terminal**

    $ ipython3


Now that we've learned the elements of what make up a regex, let's try writing one for gender information.

### 1

The first thing we do is import the `re` library. This is a builtin utility library in Python for regexes.

    import re

### 2

Then, let's actually go an define our regex.
>>>email_regex = r"\b\S+@\S+\.\S+\b"

This is just one example; you might have a more comprehensive regex, but for now, it'll do the job.

Notice here we used a raw string in Python. In general, whenever you define a regex in Python, you use a raw string, which has that `r` in front of the first quote. This is so that the escape characters are treated
appropriately.

### 3

Now, let's define some test strings we can actually user to demonstrate this.

    has_email = "I would like a proper justification as to why my application for a new credit card was rejected. Please email me, Joe Higgins, at joe.higgins@provider.com."
    no_email = "This is no email information here"

### 4

Alright, let's put our regex to the test. We use the `re.search` method to do this.

    re.search(email_regex, has_email)

This method will return an object that describes the match, if it finds one; that's what we see here.
If it doesn't find a match, it'll return `None`

    re.search(email_regex, no_email)

### 4.1

So, for our purposes, what we really care about is whether or not this method returns `None`.
So we could do something like:

    re.search(email_regex, has_email) != None

And then we get `True`. And of course, if we did the same thing as above, but for `no_email`:

    re.search(email_regex, no_email) != None

We get `False`, indicating that there was no match. As expected.


### 5

Now, let's say we want to do a find and replace. For this, we want to use `re.sub`, which will actually replace
all instances that match the regex with a string you specify. Here's how it looks.

    re.sub(email_regex, "[EMAIL REDACTED]", has_email)

So the instances of `man` and `women` have been replaced.

### 6
And, if we passed in `no_email`, then:

    re.sub(email_regex, "[EMAIL REDACTED]", no_email)

The string wouldn't change at all.


### 7

So there we have it; this is how we can detect if a string has a particular type of sensitive data, with a regex,
and actually remove that sensitive data.
>>>