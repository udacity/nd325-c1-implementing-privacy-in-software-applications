#
# NOTE: Just because you pass these tests doesn't necessarily mean your data minimization implementation is correct.
# Please see the solution guide and compare your solution with the ones here.
#
from src.main.privacy import obfuscated_national_id, encrypt_email_address, decrypt_email_address, \
    encrypt_incarceration_status, decrypt_incarceration_status


class TestPrivacySanity:

    #
    # Exercise 1
    #

    def test_obfuscate_national_id(self):
        national_id = "111-11-1111"
        obfuscated_id = obfuscated_national_id(national_id)

        assert national_id not in obfuscated_id
        assert obfuscated_id not in national_id

    #
    # Exercise 2
    #

    def test_encrypt_email_address(self):
        plaintext_email_address = "myemail@email.com"
        encrypted_email_address = encrypt_email_address(plaintext_email_address)

        assert plaintext_email_address not in encrypted_email_address
        assert encrypted_email_address not in plaintext_email_address

    def test_email_address_encryption_inversion(self):
        plaintext_email_address = "myemail@email.com"
        encrypted_email_address = encrypt_email_address(plaintext_email_address)
        decrypted_email_address = decrypt_email_address(encrypted_email_address)

        assert plaintext_email_address == decrypted_email_address

    #
    # Exercise 3
    #

    def test_encrypt_incarceration_status(self):
        plaintext_incarceration_status = True
        encrypted_incarceration_status = encrypt_incarceration_status(plaintext_incarceration_status)

        assert plaintext_incarceration_status not in encrypted_incarceration_status
        assert encrypted_incarceration_status not in plaintext_incarceration_status

    def test_encrypt_incarceration_status_nondeterminism(self):

        # Check that encrypting true is non-deterministic
        true1 = encrypt_incarceration_status(True)
        true2 = encrypt_incarceration_status(True)
        true3 = encrypt_incarceration_status(True)

        assert true1 != true2
        assert true2 != true3
        assert true1 != true3

        # Check that encrypting false is non-deterministic
        false1 = encrypt_incarceration_status(False)
        false2 = encrypt_incarceration_status(False)
        false3 = encrypt_incarceration_status(False)

        assert false1 != false2
        assert false2 != false3
        assert false1 != false3

    def test_incarceration_status_encryption_inversion(self):
        plaintext_incarceration_status = True
        encrypted_incarceration_status = encrypt_incarceration_status(plaintext_incarceration_status)
        decrypted_incarceration_status = decrypt_incarceration_status(encrypted_incarceration_status)

        assert plaintext_incarceration_status == decrypted_incarceration_status


