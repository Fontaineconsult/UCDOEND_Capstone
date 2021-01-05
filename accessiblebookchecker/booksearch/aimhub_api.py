import requests
##! set to none before upload

aimhub_key = None


def init_api_key():
    global aimhub_key
    if aimhub_key is None:
        get_key = open_aimhub_session()
        aimhub_key = get_key
        print(aimhub_key)
        close_aimhub_session()

# def recheck_api_key():
#     ##! Add token recheck feature
#     pass


def open_aimhub_session():

    aimhub_login_token = requests.post('https://api.aimhub.org/api/auth/login/',
                                       json = {
                                                "email": "amp@sfsu.edu",
                                                "password": "Revert!!!"
                                       }
                                       )

    print(aimhub_login_token.request.body)

    if aimhub_login_token.status_code == requests.codes.ok:
        print("Setting Aimhub token", aimhub_login_token.status_code, aimhub_login_token.json()['key'] )
        return aimhub_login_token.json()['key']
    else:
        print("Couldn't Set Aimhub Token", aimhub_login_token.status_code)


def close_aimhub_session():
    return requests.get('https://api.aimhub.org/api/auth/logout/')


class AimHubHolding:

    def __init__(self, isbn):

        self.isbn = isbn
        self.api_key = aimhub_key
        self.title = None
        self.author = None
        self.edition = None
        self.imprint = None
        self.available = None
        self.error = None
        self.aimhub_isbn_search()

    def aimhub_isbn_search(self):
        access_token = self.api_key
        payload = {'q': self.isbn}

        if self.api_key is not None:
            headers = {'authorization': 'Token ' + access_token}
            aimhub_isbn_search = requests.get('https://api.aimhub.org/api/search?', params=payload, headers=headers)

            if aimhub_isbn_search.status_code == requests.codes.ok:
                self.construct_holding(aimhub_isbn_search.json())
            elif aimhub_isbn_search.status_code == requests.codes.too_many or \
                    aimhub_isbn_search.status_code == requests.codes.unauthorized:
                print("aimhub error ", aimhub_isbn_search.status_code)
                self.error = True
            else:
                print("aimhub error ", aimhub_isbn_search.status_code)
        else:
            print("No API Key set")
            self.error = True

    def construct_holding(self, search_results):
        if search_results['count'] > 0:
            self.title = search_results['results'][0]['title']
            self.author = search_results['results'][0]['authors']
            self.edition = search_results['results'][0]['edition']
            self.imprint = search_results['results'][0]['publisher_str']
            self.available = True
        else:
            self.available = False



