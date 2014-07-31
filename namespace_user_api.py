from bottle import Bottle, response, request
from mongoengine.errors import NotUniqueError, ValidationError
from oauth2_bottle_app import oauth2_app, oauth2_secured
from rfc6749.oauth2_errors import OAuth2Error, error
from rfc6749.Tokens import AccessToken
from namespace_models.User import User
from namespace_utils.bottle_helpers import from_params_or_json

user_api = Bottle(catchall=False, autojson=True)
user_api.merge(oauth2_app)

__version__ = '0.0.1'


@user_api.hook('after_request')
def enable_cors():
    response.headers['Access-Control-Allow-Origin'] = '*'


@oauth2_secured()
@user_api.route('/api/v1/user')
@user_api.route('/api/v1/user/<email>')
def profile(email=None):
    if email:
        # TODO: RBAC here
        if email != AccessToken().email_from_token(from_params_or_json(request, 'access_token')):
            return error(response, 'access_denied', 'You cannot access another user\'s profile')
    else:
        email = AccessToken().email_from_token(from_params_or_json(request, 'access_token'))

    try:
        return {'user': User.objects(email=email).first().email}
    except (ValidationError, NotUniqueError) as e:
        return error(response, 'server_error', e.message)
    except OAuth2Error as e:
        message = dict(e.message)
        response.status = message.pop('status_code')
        return message


if __name__ == '__main__':
    user_api.run(host='0.0.0.0', port=5555, debug=True)
