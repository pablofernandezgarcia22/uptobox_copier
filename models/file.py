from dateutil.parser import parse
import time
class File:

    def __init__(self, json, folder_path, folder_code):
        self.code = json["file_code"]
        self.name = json["file_name"].replace("'","''")
        self.size = json["file_size"]
        self.downloads = json["file_downloads"]
        self.create_date = json["file_created"]
        self.create_date_tm = time.mktime(parse(self.create_date).timetuple())
        #self.last_download = json["file_last_download"]
        #self.last_download_tm = time.mktime(parse(self.last_download).timetuple())
        self.folder_path = folder_path
        self.folder_code = folder_code