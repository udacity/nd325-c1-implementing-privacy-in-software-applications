

# Deterministic Encryption in Python


### Setting the stage

Let's walk through how to perform deterministic encryption in Python. I'm doing this all on my local machine, but you'll actually be implementing something similar in a Udacity workspace in just a bit.

Now, in this lesson we're going to be encrypting Phone Numbers, instead of hashing them like we did in the last demo. We'll be using the 256-bit AES SIV encryption algorithm.

### 1. Standardize your input

#### Explanation
The first thing we want to do is standardize our input, just like last time for hashing. This, again, is to preserve data associativity.

#### Implementation
Basically, all we're going to do is remove dashes, parentheses, periods, spaces and plus signs. We're actually going to use the `re` library again here, from our time with regex.

Here's the line of code that'll accomplish this.
```
import re
...
    sanitized_phone_number = re.sub(r"\s|\.|-|\(|\)|\+", "", plaintext_phone_number)
```

### 2. Expected Bytes

Now, because we're using 256-bit AES SIV encryption, and there 8 bits in a byte, we're going to need 256 divided by 8 bytes, which ends up being 32 bytes.
AES SIV actually requires its key to be _twice_ as long as this, so we're going to need a key that has 64 bits.

For now, let's just define this variable here:

```
    ...
    expected_bytes = int(256 / 8)   # For 256-bit AES SIV 
```

### 3. Defining our Key

#### Existing Key
Now, let's use this information to define our key. This is very similar to defining and storing our PEPPER for hashing. We're going to get the secret key, if we can, from our secret registry.

```
    encryption_key = get_secret_bytes("Phone Number Encryption Key")
```

#### New Key

If we cannot, because it hasn't been defined, we create it. Except, this time we're going to use the `get_random_bytes` method from the `Crypto.Random` library.
```
from Crypto.Random import get_random_bytes
...
    if not encryption_key:
        encryption_key = get_random_bytes(expected_bytes * 2)
        overwrite_secret_bytes("Phone Number Encryption Key", encryption_key)
```
Remember, the reason that we're multiplying the number of bytes by 2 is because AES SIV requires this.

### 4. Create the Cipher

Once we have the key figured out, we're actually going to make a cipher object, which is going to do the heavy lifting of the encryption and decryption. To do this, we're going to use the `Crypto.Cipher` library

```
from Crypto.Cipher import AES
   ...
   cipher = AES.new(encryption_key, AES.MODE_SIV)
   cipher.update(b"")
```
The first line there actually creates a new cipher in the `SIV` mode, with our encryption key. The second line add in something called a header - we actually don't care about this at all because it's meant to be used for encrypted values that require verification when sending encrypted messages, and we're not actually sending any messages elsewhere here. So we just pass in an empty byte string.

### 5. Encrypt and Digest

#### Initial
Now, we use that cipher that has our encryption key specified in it, and we actually pass in our plaintext input into it, encoded as a utf-8 byte string.
```
    ciphertext, tag = cipher.encrypt_and_digest(sanitized_phone_number.encode("utf-8"))
```
From this, we get our ciphertext and our tag. This tag thing is also meant for verification, and is a required part of AES SIV. For our purposes, you can just think of it as an extension of the ciphertext that we have to keep around.


#### Decoded

Now, `ciphertext` and `tag` are both byte strings, and we need to convert them into actual strings so that we can return them. What we're going to do is standardize the bytes as base 64 encoded bytes, and then decode them into a string using utf-8. If that sounded like gibberish to you, don't worry; this is just string and byte wrangling; it sadly is a necessary evil of cryptography, and therefore, of privacy engineering. But as long as you follow what we're doing here for this `Crypto.Cipher` library, you should be fine.
```
    ciphertext_str = b64encode(ciphertext).decode("utf-8")
    tag_str = b64encode(tag).decode("utf-8")
```

#### Return
Finally, we're going to wrap the cipher text and the tag into a dictionary and convert that to a json string.
```
import jsons
    ...
    return jsons.dumps({'ciphertext': ciphertext_str, 'tag': tag_str})
```

### 6. Decryption Start

Alright. Now we've done encryption. Let's give decryption a shot. From our encrypted phone number string, let's get out our cipher text and our tag, and convert them back to bytes.

```
    ciphertext_and_tag_strings = jsons.loads(encrypted_phone_number)
    ciphertext = b64decode(ciphertext_and_tag_strings['ciphertext'].encode("utf-8"))
    tag = b64decode(ciphertext_and_tag_strings['tag'].encode("utf-8"))
```
Again, don't sweat about the `b64decode` and the encoding with UTF-8 here; we're just doing the inverse of what we did in the encryption method to get back to the same state we were in before we packaged those up into a string.

### 7. Get the key

After this, we're going to get the key from our secret registry. Remember, if we're calling the decryption method, that means someone probably did encryption before, so the key _must_ be in the secret store. So this time, we can just get away with:

```
    encryption_key = get_secret_bytes("Phone Number Encryption Key")
```

### 8. Build the cipher

Now, we're going to build our cipher, just like we did above. Again we're still using `SIV` mode, and we're going to call the `update` method with an empty byte string.
```
    cipher = AES.new(encryption_key, AES.MODE_SIV)
    cipher.update(b"")
```

### 9. Decrypt and Return

And finally, we're going to decrypt and return our string. We're going to call the `decrypt_and_verify` method on the `ciphertext` and the `tag`. This gives us back bytes, so we decode that into a `utf-8` string to get back the original value.

```
    return cipher.decrypt_and_verify(ciphertext, tag).decode("utf-8")
```

### 10. Try in Terminal

```
>>> encrypt_phone_number("111-111-1111")
'{"ciphertext": "AJKpN4t4pt/DZA==", "tag": "qB1ezIw6S4IKlhnKvO4sVg=="}'
>>> encrypt_phone_number("1111111111")
'{"ciphertext": "AJKpN4t4pt/DZA==", "tag": "qB1ezIw6S4IKlhnKvO4sVg=="}'
>>> decrypt_phone_number(_)
'1111111111'
```

### 11. Adding Non-determinism

All we have to do, to add non-determinism, is to add this thing called a nonce, which is very much like a salt for hashing; just a random set of bytes that is not a secret, and is entry-specific. A nonce literally is just a random string, and in our case, we want it to be 32-bytes long as well.

```
nonce = get_random_bytes(expected_bytes)
cipher = AES.new(encryption_key, AES.MODE_SIV, nonce=nonce)
```

... and then we actually have to return the nonce. Remember, like a salt it's not a secret.

```
nonce_str = b64encode(nonce).decode("utf-8")
return jsons.dumps({'ciphertext': ciphertext_str, 'tag': tag_str, 'nonce': nonce_str})
```

Then, for decryption, we just read the nonce, and use it for our cipher

```
nonce = b64decode(ciphertext_and_tag_strings['nonce'].encode("utf-8"))
cipher = AES.new(encryption_key, AES.MODE_SIV, nonce=nonce)
```

### 12. Testing in Terminal

```
>>> encrypt_phone_number("111-111-1111")
'{"ciphertext": "A623KbfHiWL50w==", "tag": "NirONlrslibi4gdLs5kTkg==", "nonce": "8sIgO1h2uK8Pemb47+p1OURbPxA6KeWdRDeyyskI90w="}'
>>> encrypt_phone_number("111-111-1111")
'{"ciphertext": "FnVTmGx9bvWrvg==", "tag": "UY9y2AaPSQ3TsQfoEKRPiw==", "nonce": "v46YgzVYS36PmFK+/7t8BsmRwT8xBX6rxrRQcD3jAPQ="}'
>>> decrypt_phone_number(_)
'1111111111'
```