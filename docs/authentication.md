# Authentication

Authentication is the mechanism of associating an incoming request with a set
of identifying credentials, such as the user the request came from, or the
token that it was signed with. The permission policies can then use those
credentials to determine if the request should be permitted.

## Configuring authentication

To configure the authentication policy globally, include a list of
authenticators when creating the application.

    app = App(__name__, authenticators=[...])

It's important to remember that including authentication by itself will not
prevent an unauthenticated request from running. You should make sure to also
include an appropriate list of permission policies.

    app = App(__name__, authenticators=[...], permissions=[is_authenticated()])

To configure the authentication policy for a particular view, include a list of
authenticators when routing to the view.

    app.get('/organisations/', authenticators=[...])
    def list_organisations():
        ...

# API Reference

## basic_auth

This authenticator provides HTTP Basic Authentication.

The authenticator must be created with a single argument, which is the user
lookup function. This function should accept a pair of `username` and `password`
arguments, and return some form of user instance if the credentials are valid.

    def lookup_username(username, password):
        """
        A mock backend for `basic_auth()`.
        """
        if username == 'admin' and password == 'password':
            return 'admin'
        return None

    app = App(
        __name__,
        authenticators=[basic_auth(lookup_username)]
    )

## token_auth

This authenticator provides a simple token-based authentication scheme.

For clients to authenticate, the token key should be included in the
Authorization HTTP header. The key should be prefixed by the string literal
"Token", with whitespace separating the two strings. For example:

    Authorization: Token 9944b09199c62bcf9418ad846dd0e4bbdfc6ee4b

The authenticator must be created with a single argument, which is the token
lookup function. This function should accept a single `token` argument,
and return some form of user instance if the token is valid.

    def lookup_token(token):
        """
        A mock backend for `token_auth()`.
        """
        if token == 'example':
            return 'admin'
        return None

    app = App(
        __name__,
        authenticators=[token_auth(lookup_token)]
    )

## Custom authenticators

An authenticator is any *callable* that takes a single `request` argument,
and does one of three things.

* Return `None` if no credentials were presented. This will allow any other
authenticators to run. The request will continue to run,
* Raise `AuthenticationFailed` if an invalid or incorrect set of credentials
were presented.
* Return some form of user instance if the credentials were correctly authenticated.
These
