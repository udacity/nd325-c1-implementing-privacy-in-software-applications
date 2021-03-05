# Hashing with a Pepper in Python Demo


Let's walk through how to hash data with a pepper in Python. I'm doing this all on my local machine, but you'll actually be implementing something similar in a Udacity workspace in just a bit.

### Secret Registry
Before we can continue, however, I do want to show you the secret store, where we're going to store our pepper. As you may remember from the previous videos, peppers are _secret_ values that are not stored in the database. Rather, they're stored on a separate machine that is totally independent of the database, usually as an environment variable.
For the purposes of this course, what we're going to do is use this store that we call our "secret registry". All the coming exercises, and the final project already have this file defined for you, and you're free to use these methods to store and retrieve your secrets.


### Setting the stage
Now, in this lesson we're going to be hashing Phone Numbers. Later on in the lesson, I'll be telling you a real world example where we actually hashed phone numbers of customers of a telecommunications company for verification in order to protect privacy. What we're doing here is going to be similar to what we did to protect their privacy.

### 1. Standardize your input

#### Explanation
The first thing we want to do is standardize our input. Remember, if the phone number if formatted differently, even if the actual phone number if the same, the hash function will create a totally different hash, which undermines our ability to associate like phone numbers.

For example (in the docstring)
```
>>> hash_phone_number("111-111-1111") == hash_phone_number("(111) 111-1111")
```
we want the hashes of these phone numbers to be the same, because they are the same number, but they're just formatted differently.

#### Implementation
Basically, all we're going to do is remove dashes, parentheses, periods, spaces and plus signs. We're actually going to use the `re` library again here, from our time with regex.

```
import re

...
    sanitized_phone_number = re.sub(r"\s|\.|-|\(|\)|\+", "", phone_number)
```
So here, any time we find any of these characters described in the regex, we're going to replace it with an empty string; so we're basically going to get rid of them.

### 2. Defining our Pepper

After this, we want to define our pepper. We can actually use the `overwrite_secret_str` method from the secret registry we have provided in order to do this.
We're also going to be using the `bcrypt` library, which is a general cryptography library in Python.

#### New Pepper

```
import bcrypt
...
    pepper = bcrypt.gensalt()
    overwrite_secret_bytes("Phone Number Pepper", pepper)
```
Note here; we're using the `gensalt` method from `bcrypt`, even though we're using a pepper. This is because the composition of a salt and pepper are the same. The real distinction is that a salt is not a secret, and is stored per entry, while a pepper is a secret, and is stored per system. But under hood, they're both just random bytes.
So here, I'm writing my pepper, which is just a collection of random bytes, to my secret store.

#### Old Pepper
However, it's important that every time, we use the _same_ pepper. We don't want to keep randomly generating peppers every time we hash, because then we're just hashing random things. We want the pepper to be the same.

```
    pepper = get_secret_bytes("Phone Number Pepper")
    if not pepper:
        pepper = bcrypt.gensalt()
        overwrite_secret_bytes("Phone Number Pepper", pepper)
```
So now, we try to get the secret pepper that corresponds to the phone number. If there's nothing there, then we overwrite it with a new one. This would only happen the first time we use the hash function on a particular machine.


### 3. `bcrypt.hashpw`

#### Initial

Now, all we have to do is use `bcrypt`'s `hashpw` method.

```
    return bcrypt.hashpw(sanitized_phone_number, pepper)
```
We pass in the string we want to hash, and our pepper or salt, which in this case is a string.

#### Fixing error
Now, the only issue here is that the `hashpw` method actually takes in bytes, not strings. In Python, bytes are actually a separate type. Currently, our pepper is already a bytes object, but our phone number is actually a string. To handle this, we're actually going to encode our string with the UTF-8 encoding format. If you don't know what UTF-8 encoding is, don't worry too much about it; it's just one way out of many to convert a collection of bytes into a string, and is used across languages.
```
    return bcrypt.hashpw(sensitive_national_id**.encode("utf-8")**, pepper)
```

#### Returning a string
But not only does `hashpw` want bytes as inputs, it also returns us bytes. To fix this, we'll change these bytes into a string by decoding, again using the `utf-8` format to do this.

```
    return bcrypt.hashpw(sensitive_national_id.encode("utf-8"), pepper).decode("utf-8")
```

### 4. In terminal

So now that we have this, let's see how this works in our terminal.

```
$ cd hashing_python
$ ipython3 -i hashing.py
```

Let's first try to hash a phone number.

```
>>> hash_phone_number("111-111-1111")
'$2b$12$SCXIEGJmI2.ZwDhQRKcDBORjb8kiLCwkVcnEp9FDjoltGqeAatzdG'
>>> hash_phone_number("111-111-1111")
'$2b$12$SCXIEGJmI2.ZwDhQRKcDBORjb8kiLCwkVcnEp9FDjoltGqeAatzdG'
>>> hash_phone_number("(111) 111 1111")
'$2b$12$SCXIEGJmI2.ZwDhQRKcDBORjb8kiLCwkVcnEp9FDjoltGqeAatzdG'
```
If you look closely, you'll see that these hashes are actually the same. Now it's try it for a different value.

```
>>> hash_phone_number("222-222-2222")
'$2b$12$98OBsFdqKs0Kk/3rEtsP0uPwB9g1EjHqMA4dUS8hG5QcnVv.av6Ke'
```
This looks the same in the beginning, but if you look at the ending characters, it's actually different.

### 5. Conclusion

So there you have it. That's hashing with a secret pepper. If you wanted to hash with a salt, the logic is the same, except instead of storing a secret pepper, you'd store your non-secret salts in your database where there would be a unique salt for each user.