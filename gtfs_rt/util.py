import os
import shutil

import requests

from gtfs_rt.config import INPUT_PATH


def download_file(url, filename):
    with requests.get(url, stream=True) as r:
        with open(os.path.join(INPUT_PATH, filename), 'wb') as f:
            shutil.copyfileobj(r.raw, f)
