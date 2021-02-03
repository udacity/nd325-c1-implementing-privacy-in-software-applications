
class Candidate:
    """
    A candidate for a job position
    """
    def __init__(self, internal_id: int, name: str, email: str):
        self.internal_id = internal_id
        self.name = name
        self.email = email
