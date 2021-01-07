from secrets import token_urlsafe

from requests import post

from config import client_id, client_secret

class Auth():
    def __init__(self):
        self.code_verifier = self.code_challenge = token_urlsafe(100)[:128]
    
    def getlink(self):
        parameters = {
            'response_type': 'code',
            'client_id': client_id,
            'client_secret': client_secret,
            'code_challenge': self.code_challenge
            # 'state': 'RequestID42',
            # 'redirect_uri': 
            # 'code_challenge_method':
        }
        parameters='&'.join(['='.join(i) for i in parameters.items()])
        link=f'https://myanimelist.net/v1/oauth2/authorize?{parameters}'

        return link

    def gettoken(self, code):
        parameters = {
            'client_id': client_id,
            'client_secret': client_secret,
            'code': code,
            'code_verifier': self.code_verifier,
            'grant_type': 'authorization_code'
        }

        r = post('https://myanimelist.net/v1/oauth2/token', data=parameters).json()

        return r['access_token']