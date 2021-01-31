from main.pii_detection import redact_phone_numbers


class TestRegexRedaction:

    def test_id_number_redaction_vanilla(self):
        """
        Checks that phone number redaction works
        """
        original_text = """My Id number is 12306.""".strip()
        expected_redacted_comment = """My Id number is [REDACTED PHONE NUMBER].""".strip()
        assert redact_phone_numbers(original_text) == expected_redacted_comment

    def test_id_number_redaction_special_id_number(self):
        """
        Checks that phone number redaction works
        """
        original_text = """My Id number is 125645331.""".strip()
        expected_redacted_comment = """My Id number is [REDACTED PHONE NUMBER].""".strip()
        assert redact_phone_numbers(original_text) == expected_redacted_comment

    def test_id_number_redaction_removed_id_number(self):
        """
        Checks that phone number redaction works
        """
        original_text = """The amusement park's zip code is 11305.""".strip()
        expected_redacted_comment = original_text
        assert redact_phone_numbers(original_text) == expected_redacted_comment

    def test_id_number_redaction_4(self):
        """
        Checks that phone number redaction works
        """
        original_text = """The amusement park's zip code is 95054.""".strip()
        expected_redacted_comment = original_text
        assert redact_phone_numbers(original_text) == expected_redacted_comment


