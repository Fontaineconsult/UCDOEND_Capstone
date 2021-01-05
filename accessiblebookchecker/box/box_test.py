from boxsdk import OAuth2, Client, object

auth = OAuth2(

    client_id="zamp86vr1wge5m2p5txtmwiyv0sfwtes",
    client_secret="zamp86vr1wge5m2p5txtmwiyv0sfwtes",
    access_token="PsW35EPbyde4vBMGw4wz4xpzSx7qEKyX" #expires after 60 min


)


client = Client(auth)


# https://sfsu.app.box.com/s/dk0bwi0aslvsyup7df94hj5xvluvx4xq


test = client.get_shared_item('https://sfsu.app.box.com/s/dk0bwi0aslvsyup7df94hj5xvluvx4xq')
print(test.__dict__)

file_content = client.file('659890998652').content()


# folder = client.folder('18254957996').get()
#
#
# print(folder["item_collection"]['entries'][4].content())