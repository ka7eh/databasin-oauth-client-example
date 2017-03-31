from social_core.backends.oauth import BaseOAuth2


class DataBasinOAuth(BaseOAuth2):
    """ OpenID Connect backend designed for use with the Open edX auth provider. """

    name = 'databasin'

    AUTHORIZATION_URL = 'http://databasin.local:8000/openid/authorize/'
    ACCESS_TOKEN_URL = 'http://databasin.local:8000/openid/token/'
    USERINFO_URL = 'http://databasin.local:8000/openid/userinfo/'
    ACCESS_TOKEN_METHOD = 'POST'
    ID_KEY = 'sub'
    DEFAULT_SCOPE = ['openid', 'profile', 'email']

    PROFILE_TO_DETAILS_KEY_MAP = {
        'nickname': 'username',
        'email': 'email',
        'given_name': 'first_name',
        'family_name': 'last_name'
    }

    def get_user_details(self, response):
        """Maps key/values from the response to key/values in the user model.
        Does not transfer any key/value that is empty or not present in the response.
        """
        details = {}
        for source_key, dest_key in self.PROFILE_TO_DETAILS_KEY_MAP.items():
            value = response.get(source_key)
            if value is not None:
                details[dest_key] = value

        return details

    def user_data(self, access_token, *args, **kwargs):
        try:
            return self.get_json(self.USERINFO_URL, headers={'Authorization': 'Bearer {}'.format(access_token)})
        except ValueError:
            return None
