import os
import requests
import urllib.parse
TOKEN = os.environ["TOKEN"]


def get_folder_structure(path, offset):
    path = urllib.parse.quote(path)
    url = "https://uptobox.com/api/user/files?token=%s&orderBy=transcoded&dir=desc&offset=%i&path=%s&limit=100" % (TOKEN,offset, path)
    resp = requests.get(url)
    return resp.json()

def get_url(token,code):
    url = "https://uptobox.com/api/link?token=%s&file_code=%s" % (token, code)
    resp = requests.get(url)
    return resp.json()["data"]["dlLink"]

def copy_files(destination_folder, files_code ):
    url = "https://uptobox.com/api/user/files"
    #files_code="so2a8ls1t6en,hymhqat1fqh9,92nq6cngpfcm,wbqn48ojpxcw,hz6425rq3uvs,67abkb06picd,pf81s8vltjuc,6o59an7f4mp7,oel8nymryuq9,yufhemsjv76n"


    data = {"token":TOKEN,
    "file_codes":",".join(files_code),
    "destination_fld_id":destination_folder,
    "action":"copy"}

    print(data)
    resp = requests.patch(url,json=data)

    
    print(resp.json())

def create_folder(path, folder_name ):
    url = "https://uptobox.com/api/user/files"

    data = {"token":TOKEN,"path":path,"name":folder_name}
    #data = {"token":"5dacd15039bb7a5a4e4ea8e45e07e0179mw5h","path":"//Servidor2","name":"prueba"}
    print(data)
    
    print("Creating folder")
    resp = requests.put(url,json=data)
    print(resp.json())
