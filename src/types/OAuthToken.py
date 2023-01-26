class OAuthToken:
    def __init__(self, access_token, token_type, expires_at_seconds, refresh_token, refresh_expires_at_seconds, membership_id):
        self.access_token = access_token
        self.token_type = token_type
        self.expires_at_seconds = expires_at_seconds
        self.refresh_token = refresh_token
        self.refresh_expires_at_seconds = refresh_expires_at_seconds
        self.membership_id = membership_id
