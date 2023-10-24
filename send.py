import json

import requests

FEED_ID = "cl-concepcion"
ACCESS_TOKEN = "mSLhl7aa.qNcLxLwW7ZRTTXapWdlQjxjXLD7KGeRR"

GTFSRT_DEBUG_URL = 'https://routemanager.dtpr.dev.transapp.cl/api/v2/gtfs-rt/{feed_id}/'


def get_gtfs_rt_data():
    return open('./output/data.proto', 'rb')


def send_data():
    headers = {
        'Authorization': 'Api-Key {0}'.format(ACCESS_TOKEN)
    }
    gtfs_rt_data_file = get_gtfs_rt_data()

    url = GTFSRT_DEBUG_URL.format(feed_id=FEED_ID)
    files = {
        'data': gtfs_rt_data_file
    }
    response = requests.post(url=url, headers=headers, files=files)
    print(response.status_code)
    print(json.loads(response.content))

    gtfs_rt_data_file.close()


if __name__ == '__main__':
    send_data()
