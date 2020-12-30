from backend.main.objects.voter import Voter


class TestMinimization:

    def test_voter_minimization_consistency(self):
        """
        Checks to make sure that the obfuscated voter ID is consistent across hashes
        """
        voter = Voter("Adam", "Smith", "111111111")
        minimal_voter = voter.get_minimal_voter()

        obfuscated_natl_id = minimal_voter.obfuscated_national_id

        assert minimal_voter.first_name == voter.first_name
        assert minimal_voter.last_name == voter.last_name

        for _ in range(10):
            current_obfuscated_natl_id = voter.get_minimal_voter().obfuscated_national_id
            assert obfuscated_natl_id == current_obfuscated_natl_id
