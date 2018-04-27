import logging
from oauthlib import oauth2
from ..models import users


logger = logging.getLogger(__name__)


class AuthnadoValidator(oauth2.RequestValidator):

    ############################
    # Authorization request
    ############################

    def validate_client_id(self, client_id, request, *args, **kwargs):
        """
        Check if the client exists.
        """
        logger.debug('VALIDATE CLIENT: {}'.format(client_id))
        client = getattr(request, 'client', None)
        if client is None:
            client = users.Client(
                client_id=client_id, client_secret='world'
            )
            # TODO: Fetch the client from the database.
            #       Return false if it does not exist.
            # return False
        request.client = client
        return True

    def get_default_scopes(self, client_id, request, *args, **kwargs):
        # Scopes a client will authorize for if none are supplied in the
        # authorization request.
        client = getattr(request, 'client', None)
        if client is None:
            client = users.Client(
                client_id='hello', client_secret='world'
            )
        scopes = client.default_scopes
        logger.debug('GET DEFAULT SCOPES: client_id={} scopes={}'.format(
            client_id, scopes
        ))
        return scopes

    def validate_scopes(self, client_id, scopes, client, request,
                        *args, **kwargs):
        # Is the client allowed to access the requested scopes?
        return set(client.default_scopes).issuperset(set(scopes))

    def get_default_redirect_uri(self, client_id, request, *args, **kwargs):
        return request.client.default_redirect_uri

    def validate_response_type(self, client_id, response_type, client, request,
                               *args, **kwargs):
        # if response_type == "code":
        #     return client.allows_grant_type(AbstractApplication.GRANT_AUTHORIZATION_CODE)
        # elif response_type == "token":
        #     return client.allows_grant_type(AbstractApplication.GRANT_IMPLICIT)
        if response_type in ['code', 'token']:
            return True
        return False

    ############################
    # Token request
    ############################

    def authenticate_client(self, request, *args, **kwargs):
        request.client = users.Client(
            client_id='hello', client_secret='world'
        )
        return True

    def validate_grant_type(self, client_id, grant_type, client, request,
                            *args, **kwargs):
        """
        Ensure the client is authorized to use the requested grant type.

        Available grant types:

        * authorization_code
        * password
        * client_credentials
        * refresh_token
        """
        if grant_type not in client.allowed_grant_types:
            return False
        return True

    def save_bearer_token(self, token, request, *args, **kwargs):
        logger.debug('SAVE BEARER TOKEN: {}'.format(token))
        # self._tokensetter(token, request, *args, **kwargs)
        return request.client.default_redirect_uri


server = oauth2.Server(AuthnadoValidator())
