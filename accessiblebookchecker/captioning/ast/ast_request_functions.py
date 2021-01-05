import requests
import json

token = "Bearer 7048d1179fecde472a6ce01145b92699f09a729762894de6620acb1bdfc7049b55a65b735f9d8c2ca1224742a85a48c5-13e864bf-f1b3-11e8-ab84-00505602114a"

def authenticate():
    CustomerID = "sfsudev"
    PartnerType = "dprcCaptioningManagerTest"
    CustomerSecret = "37533m4AC-1088b9F50BF-1671w3-78B12e3"

    authenticate = "https://sandboxapi.automaticsync.com/v1/authenticate"

    payload = {"method": "authenticate", "params":{ "PartnerType": PartnerType,
                                                   "CustomerID": CustomerID,
                                                   "CustomerSecret": CustomerSecret}
               }
    auth_request = requests.post(authenticate, data=json.dumps(payload))
    print(auth_request.content)
    return auth_request


authenticate()

def get_submissions():
    get_submissions = "https://sandboxapi.automaticsync.com/v1/submissions"
    params = {"method": "list",
              "params": {"Limit": "10"}}

    header = {"Authorization": token}

    get_list = requests.post(get_submissions, data=json.dumps(params), headers=header)
    print(get_list.headers)
    print(get_list.content)



def submit_job_to_ast():
    submit_url = "https://sandboxapi.automaticsync.com/v1/submissions"
    header = {"Authorization": token}

    params = {"method":"create",
              "params": {"App":"Captioning",
                         "Description":"Test Desc",
                         "Language":"English",
                         "Notes":"Test test test test",
                         "Rush":"T",
                         "HaveTrans":"N",
                         "PersistentNote": 0,
                         "TransExpert": 0,
                         "CallBack":"https%3A%2F%2Famp.sfsu.edu%2Fapi%2Fcaptioning%2Fast-cap-result-callback",
                         "StatusURL":"https%3A%2F%2Famp.sfsu.edu%2Fapi%2Fcaptioning%2Fast-cap-status-callback"}}

    submit_job = requests.post(submit_url, data=json.dumps(params), headers=header)
    print(submit_job.headers)
    print(submit_job.content)



def submit_url_to_ast():
    list_url = "https://sandboxapi.automaticsync.com/v1/lists"
    header = {"Authorization": token}
    params = {"method": "create",
              "params": {"Description":"Example Test Mega Fun Version",
                        "Rush": "N",
                        "App":"Captioning",
                        "ListItem": [{"URL":"https://www.youtube.com/watch?v=-spgUfGFTSY",
                                      "BaseName":"Tizzesssttt",
                                      "CallBack":"https%3A%2F%2Famp.sfsu.edu%2Fapi%2Fcaptioning%2Fast-cap-result-callback",
                                      "StatusURL":"https%3A%2F%2Famp.sfsu.edu%2Fapi%2Fcaptioning%2Fast-cap-status-callback"}],

                        }}

    list_url = requests.post(list_url, data=json.dumps(params), headers=header)
    print(list_url.content)


def get_url_submission_details():
    list_url = "https://sandboxapi.automaticsync.com/v1/lists"
    header = {"Authorization": token}

    params = {"method":"list",
              "params":{"Limit": "10"}}

    list_url = requests.post(list_url, data=json.dumps(params), headers=header)
    print(list_url.content)


def submit_media_to_ast():
    pass

