class User:
    def __init__(self, user_id: str, username: str):
        """
        Initializes a user with:
        - user_id: Unique identifier for the user
        - username: Name of the user
        """
        self.user_id = user_id
        self.username = username
        self.portfolio = set()  # Properties owned by the user
        self.shortlist = set()  # Shortlisted properties

    def add_to_portfolio(self, property_id: str):
        """Adds a property to the user's portfolio."""
        self.portfolio.add(property_id)

    def remove_from_portfolio(self, property_id: str):
        """Removes a property from the user's portfolio."""
        self.portfolio.discard(property_id)

    def add_to_shortlist(self, property_id: str):
        """Adds a property to the user's shortlist."""
        self.shortlist.add(property_id)

    def remove_from_shortlist(self, property_id: str):
        """Removes a property from the user's shortlist."""
        self.shortlist.discard(property_id)
