from dotenv import load_dotenv
load_dotenv()

import api
from models.file import File
import os


TOKEN = os.environ["SERVER_PATH"]
MAX_COPY_SIZE = int(os.environ["MAX_COPY_SIZE"])*1000000000
MAX_COPY_FILES= int(os.environ["MAX_COPY_FILES"])

def copy_queue(destination_folder_id, FILES_QUEUE):

    QUEUE = []
    QUEUE_SIZE = 0

    for x in FILES_QUEUE:
        QUEUE.append(x.code)
        QUEUE_SIZE += x.size

        if QUEUE_SIZE >= MAX_COPY_SIZE or len(QUEUE) >= MAX_COPY_FILES:
            # Copy
            api.copy_files(destination_folder_id, QUEUE)
            QUEUE = []
            QUEUE_SIZE = 0
    
def scrap_folder(path,copy_path, folder_code = 0):
    print("Analysing %s" % path)
    print("Copy to %s" % copy_path)
    FILES_QUEUE = []

    SUBFOLDERS = []
    SUBFOLDERS_CODE = []
    resp = api.get_folder_structure(path,0)
    OFFSET = 0
    FINISH_FILE_LOCATION = False
    FILES_folder = 0
    #Current folder info
    
    resp_copy = api.get_folder_structure(copy_path,OFFSET)
    CURRENT_FOLDER_ID = resp_copy["data"]["currentFolder"]["fld_id"]
    print("Copy folder id %s" %CURRENT_FOLDER_ID)
    
    while not FINISH_FILE_LOCATION:
        resp = api.get_folder_structure(path,OFFSET)
        for x in resp["data"]["folders"]:
            if x["fullPath"] not in SUBFOLDERS and "@eaDir" not in x["fullPath"]:
                SUBFOLDERS.append(x["fullPath"])
                SUBFOLDERS_CODE.append(x["fld_id"])
        for x in resp["data"]["files"]:

            f = File(x, path,folder_code )        
            FILES_QUEUE.append(f)    
            FILES_folder += 1

        FINISH_FILE_LOCATION = len(resp["data"]["files"]) != 10        
        OFFSET += 100
    print("FOLDER: "+path+" files: "+str(FILES_folder))
    copy_queue(CURRENT_FOLDER_ID,FILES_QUEUE)
    
    #scrap sub folder
    for i in range(len(SUBFOLDERS)):
        #Create folder in destination
        next_copy_dest = copy_path+'/'+SUBFOLDERS[i].split('/')[-1]
        print("Created folder: ",next_copy_dest)
        api.create_folder(copy_path,SUBFOLDERS[i].split("/")[-1] )
        scrap_folder(SUBFOLDERS[i],next_copy_dest,SUBFOLDERS_CODE[i])

# define Python user-defined exceptions
class InvalidCopyFolder(Exception):
    """Exception raised for errors in the copy folder destinatio.

    Attributes:
        message -- explanation of the error
    """

    def __init__(self, message="Error with copy folder destination"):
        self.message = message
        super().__init__(self.message)

def check_empty_folder_exists(PATH):
    print("Checking folder %s" % PATH)
    try:
        resp = api.get_folder_structure(PATH,0)
        if len(resp["data"]["folders"]) != 0 or len( resp["data"]["files"]) != 0: 
            print("Copy folder not empty")
            raise InvalidCopyFolder("Copy folder not empty")
    except InvalidCopyFolder:
            raise InvalidCopyFolder("Copy folder not empty")
    except:
        print("Copy folder does not exists")
        raise InvalidCopyFolder("Copy folder does not exists")

if __name__ == "__main__":
    print("Started program")
    #Check if copy folder is empty and exists    
    COPY_PATH = os.environ["COPY_PATH"]
    check_empty_folder_exists(COPY_PATH)

    PATH = os.environ["SERVER_PATH"]
    scrap_folder(PATH,COPY_PATH)

    print("Copy finish")