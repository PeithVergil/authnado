import json
import logging
import functools
# from datetime import datetime, timedelta
from oauthlib import oauth2
from ..models import users


logger = logging.getLogger(__name__)


class AuthnadoValidator(oauth2.RequestValidator):

    ############################
    # Authorization request
    ############################

    def __init__(self, provider, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.provider = provider

    def validate_client_id(self, client_id, request, *args, **kwargs):
        """
        Check if the client exists.

        log.debug('Validate client %r', client_id)
        client = request.client or self._clientgetter(client_id)
        if client:
            # attach client to request object
            request.client = client
            return True
        return False
        """
        logger.debug('VALIDATE CLIENT ID: {}'.format(client_id))
        client = getattr(request, 'client', None)
        if client is None:
            client = self.provider.get_client(client_id)
            if client is None:
                return False
        request.client = client
        return True

    def get_default_scopes(self, client_id, request, *args, **kwargs):
        # Scopes a client will authorize for if none are supplied in the
        # authorization request.
        client = getattr(request, 'client', None)
        if client is None:
            client = self.provider.get_client(client_id)
        scopes = client.default_scopes
        logger.debug('DEFAULT SCOPES: client={} scopes={}'.format(
            client_id, scopes
        ))
        return scopes

    def validate_scopes(self, client_id, scopes, client, request,
                        *args, **kwargs):
        # Is the client allowed to access the requested scopes?
        return set(client.default_scopes).issuperset(set(scopes))

    def get_default_redirect_uri(self, client_id, request, *args, **kwargs):
        client = getattr(request, 'client', None)
        if client is None:
            client = self.provider.get_client(client_id)
        redirect = client.default_redirect_uri
        logger.debug('DEFAULT REDIRECT URI: client={} redirect={}'.format(
            client_id, redirect
        ))
        return redirect

    def validate_code(self, client_id, code, client, request, *args, **kwargs):
        # try:
        #     grant = Grant.objects.get(code=code, application=client)
        #     if not grant.is_expired():
        #         request.scopes = grant.scope.split(" ")
        #         request.user = grant.user
        #         return True
        #     return False

        # except Grant.DoesNotExist:
        #     return False
        return True

    def confirm_redirect_uri(self, client_id, code, redirect_uri, client,
                             *args, **kwargs):
        """
        Ensure the redirect_uri is listed in the Application instance redirect_uris field
        """
        # grant = Grant.objects.get(code=code, application=client)
        # return grant.redirect_uri_allowed(redirect_uri)
        return True

    def invalidate_authorization_code(self, client_id, code, request,
                                      *args, **kwargs):
        """
        Remove the temporary grant used to swap the authorization token
        """
        # grant = Grant.objects.get(code=code, application=request.client)
        # grant.delete()

    def save_authorization_code(self, client_id, code, request,
                                *args, **kwargs):
        logger.debug('SAVE AUTH CODE: {}'.format(code))
        self.provider.set_code(request, code)

    def validate_response_type(self, client_id, response_type, client, request,
                               *args, **kwargs):
        # if response_type == "code":
        #     return client.allows_grant_type(AbstractApplication.GRANT_AUTHORIZATION_CODE)
        # elif response_type == "token":
        #     return client.allows_grant_type(AbstractApplication.GRANT_IMPLICIT)
        if response_type in ['code', 'token']:
            return True
        return False

    def validate_redirect_uri(self, client_id, redirect_uri, request,
                              *args, **kwargs):
        """
        Ensure client is authorized to redirect to the redirect_uri.
        This method is used in the authorization code grant flow and also
        in implicit grant flow. It will detect if redirect_uri in client's
        redirect_uris strictly, you can add a `validate_redirect_uri`
        function on grant for a customized validation.
        """
        # client = getattr(request, 'client', None)
        # if client is None:
        #     client = users.Client(
        #         client_id=client_id, client_secret='world'
        #     )
        #     # TODO: Fetch the client from the database.
        #     #       Return false if it does not exist.
        #     # return False
        #     request.client = client
        # return redirect_uri in client.redirect_uris
        return True

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
        self.provider.set_token(token, request, *args, **kwargs)
        return request.client.default_redirect_uri


class AuthnadoProvider:

    def __init__(self, executor):
        self.executor = executor
        self.server = oauth2.Server(AuthnadoValidator(self))

    async def validate_request(self, uri, body, method, headers):
        try:
            body = json.loads(body)
        except json.JSONDecodeError:
            pass

        # Run blocking call on a separate thread.
        return await self.executor(
            self.server.validate_authorization_request,
            uri, method,
            body, headers,
        )

    async def create_response(self, uri, scopes, credentials):
        create_authorization_response = functools.partial(
            self.server.create_authorization_response,
            uri,
            scopes=scopes,
            credentials=credentials,
        )
        # Run blocking call on a separate thread.
        return await self.executor(create_authorization_response)

    async def create_token(self, uri, body, method, headers):
        try:
            body = json.loads(body)
        except json.JSONDecodeError:
            pass

        # Run blocking call on a separate thread.
        return await self.executor(
            self.server.create_token_response,
            uri, method,
            body, headers,
        )

    def get_client(self, client_id):
        logger.debug('GET CLIENT: client_id={}'.format(client_id))
        # TODO: Fetch the client from the database.
        #       Return false if it does not exist.
        client = users.Client(
            client_id=client_id, client_secret='world'
        )
        return client

    def set_token(self, token, request, *args, **kwargs):
        """
        TODO: Save access token to the database.

        # Grab the client instance
        # in the request object.
        client = request.client
        expires = datetime.utcnow() + timedelta(seconds=token['expires_in'])
        with dbsession() as session:
            token = Token(
                token_type=token['token_type'],
                access_token=token['access_token'],
                refresh_token=token['refresh_token'],
                expires=expires,
            )
            session.add(token)
        """
        logger.debug('SET TOKEN: token={}'.format(token))

    def set_code(self, request, code):
        """
        TODO: Save auth code to the database.

        redirect = request.redirect_uri
        expires = datetime.utcnow() + timedelta(seconds=60)
        scopes = ' '.join(request.scopes)
        grant = users.Grant(
            user=request.user,
            client=request.client,
            code=code['code'],
            scopes=scopes,
            expires=expires,
            redirect=redirect,
        )
        """
        logger.debug('SET CODE: code={}'.format(code))
