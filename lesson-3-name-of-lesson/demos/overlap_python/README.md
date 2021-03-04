Let's see overlap detection in action here, again in python.

    import re


### 1
Let's look at the current state of our string from Joe Higgins:

    text = "I would like a proper justification as to why my application for a new credit card was rejected. Please email me, Joe Higgins, at [EMAIL REDACTED]"

Remember, we redacted the email address already with the previous regex.

### 2
Now, since this entry was submitted by Joe Higgins, we actually already have his information in our database, from his original application. We can go ahead and look at up. Let's say we get back, from our database, we get back his name:

    first_name = "JOE"
    middle_name = "ANDREW"
    last_name = "HIGGINS"

### 3

Let's make this into a set here.

    existing_sensitive_data = set([first_name, middle_name, last_name])
    existing_sensitive_data

Note that we might have other things in this `existing_sensitive_data` set. For example, we might add Joe's employer's name here, as we might've collected that information too, or Joe's zip code.

### 4

Perfect. Now, let's try and perform the replacement we need to perform.

    for name in existing_sensitive_data:
        text = re.sub(name, "[NAME REDACTED]", text, flags=re.IGNORECASE)

Notice here, we're actually using our old friend `re.sub` to turn the name into an explicit regex. We're also using the IGNORECASE flag to make this comparison string insensitive.

###

And once we've done that, let's see how our text looks:

    text


You'll notice that both the first and last name for Joe are redacted, as we wanted.