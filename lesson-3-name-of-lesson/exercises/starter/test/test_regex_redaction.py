from main.pii_detection import redact_phone_numbers


class TestRegexRedaction:

    def test_phone_number_redaction_1(self):
        """
        Checks that phone number redaction works
        """
        original_text = """My phone number is (345) 876-3452.""".strip()
        expected_redacted_comment = """My phone number is [REDACTED PHONE NUMBER].""".strip()
        assert redact_phone_numbers(original_text) == expected_redacted_comment

    def test_phone_number_redaction_2(self):
        """
        Checks that phone number redaction works
        """
        original_text = """My phone number is 374 378-5873.""".strip()
        expected_redacted_comment = """My phone number is [REDACTED PHONE NUMBER].""".strip()
        assert redact_phone_numbers(original_text) == expected_redacted_comment

    def test_phone_number_redaction_3(self):
        """
        Checks that phone number redaction works
        """
        original_text = """My phone number is 473-275-1677.""".strip()
        expected_redacted_comment = """My phone number is [REDACTED PHONE NUMBER].""".strip()
        assert redact_phone_numbers(original_text) == expected_redacted_comment

    def test_phone_number_redaction_4(self):
        """
        Checks that phone number redaction works
        """
        original_text = """My phone number is 3473471634.""".strip()
        expected_redacted_comment = """My phone number is [REDACTED PHONE NUMBER].""".strip()
        assert redact_phone_numbers(original_text) == expected_redacted_comment

    def test_phone_number_redaction_does_not_catch_other_numbers(self):
        """
        Checks that phone number redaction doesn't catch other numbers (non phone numbers)
        """
        original_text = """My ID number is 347347163434.""".strip()
        expected_redacted_comment = original_text
        assert redact_phone_numbers(original_text) == expected_redacted_comment

