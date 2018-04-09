class Client:

    def __init__(self, client_id, client_secret, *args, **kwargs):
        self.client_id, self.client_secret = client_id, client_secret

    @property
    def allowed_grant_types(self):
        return ['authorization_code', 'client_credentials']

    @property
    def default_scopes(self):
        return ['api', 'app']

    @property
    def default_redirect_uri(self):
        return 'http://example.com'
