import os
import shutil
import urllib.request as request
import zipfile
from pathlib import Path


class DownloadDistrict(object):
    def download_district_data(self):
        SHP_SLUG = "cb_{}_us_cd{}_500k".format(self.YEAR, self.CONGRESS)
        DOWNLOAD_PATH = os.path.join(self.DOWNLOAD_DIRECTORY, SHP_SLUG)
        ZIPFILE = "{}{}.zip".format(DOWNLOAD_PATH, SHP_SLUG)
        SHP_PATH = os.path.join(
            self.SHP_SOURCE_BASE.format(self.YEAR), SHP_SLUG
        )

        if not Path(ZIPFILE).is_file():
            with request.urlopen("{}.zip".format(SHP_PATH)) as response, open(
                ZIPFILE, "wb"
            ) as out_file:
                shutil.copyfileobj(response, out_file)

        if not Path("{}{}.shp".format(DOWNLOAD_PATH, SHP_SLUG)).is_file():
            with zipfile.ZipFile(ZIPFILE, "r") as file:
                file.extractall(DOWNLOAD_PATH)
