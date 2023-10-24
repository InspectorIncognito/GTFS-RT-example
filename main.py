import datetime
import logging
import os
from pathlib import Path
from typing import List

import requests
import typer

from gtfs_rt.config import OUTPUT_PATH, INPUT_PATH
from gtfs_rt.reader import get_gtfs_rt_entities
from gtfs_rt.util import download_file

app = typer.Typer()

logger = logging.getLogger(__name__)


@app.command()
def read_predictor_data(file_path: Path = typer.Argument(..., help='file path of predictor data'),
                        trip_id_list_with_detail: List[str] = typer.Argument(..., help='')):
    """
    Print proto file
    """
    entities = get_gtfs_rt_entities(file_path)
    for entity in entities:
        logger.info(entity.vehicle.trip.trip_id)
        if entity.vehicle.trip.trip_id in trip_id_list_with_detail:
            print(entity)

            previous = None
            is_greater = None
            for a in entity.trip_update.stop_time_update:
                if previous is not None:
                    is_greater = a.arrival.time > previous
                logger.info('{} {}'.format(a.arrival.time, is_greater))
                previous = a.arrival.time


@app.command()
def read_routemanager_data(file_path: Path = typer.Argument(..., help='file path of routemanager data')):
    """
    Print proto file
    """
    entities = get_gtfs_rt_entities(file_path)
    trip_id_list = []
    for entity in entities:
        if entity.vehicle.trip.trip_id:
            print(entity)

            trip_id = entity.vehicle.trip.trip_id
            trip_id_list.append(trip_id)

    logger.info('{0} vehicles with trip id of {1}'.format(len(trip_id_list), len(entities)))
    logger.info(' '.join(trip_id_list))

    return trip_id_list


@app.command()
def download_predictor_file():
    """
    download predictor file
    """
    url = 'https://transapp-prod-bucket.s3.us-east-2.amazonaws.com/predictions/rancagua_el_teniente_pred.proto'
    filename = 'predictor.proto'
    download_file(url, filename)


@app.command()
def download_routemanager_file():
    """
    download routemanager file
    """
    url = 'https://transapp-prod-bucket.s3.us-east-2.amazonaws.com/routemanager/cl-rancagua-det-transporte.proto'
    filename = 'routemanager.proto'
    download_file(url, filename)


@app.command()
def check_trip_id_is_realtime(trip_id_list: List[str] = typer.Argument(..., help='expedition id')):
    logger.info('checking realtime data in OTP...')
    is_realtime_counter = 0
    logger.info('route_id\tdirection_id\tshape_id\ttrip_id -> is_realtime')
    for trip_id in trip_id_list:
        url_base = 'https://otp.app.transapp.cl/otp/routers/rancagua_el_teniente/index/trips/cl-rancagua-det-transporte:'
        url = '{0}{1}'.format(url_base, trip_id)
        json_response = requests.get(url).json()

        route_id = json_response['route']['id'].split(':')[1]
        direction_id = json_response['directionId']
        shape_id = json_response['shapeId'].split(':')[1]

        url = '{0}{1}/stoptimes'.format(url_base, trip_id)
        json_response = requests.get(url).json()

        is_realtime = all(map(lambda x: x['realtime'], json_response))
        if is_realtime:
            is_realtime_counter += 1
        logger.info('{}\t{}\t{}\t{} -> {}'.format(route_id, direction_id, shape_id, trip_id, is_realtime))

    percentage = is_realtime_counter / len(trip_id_list) * 100
    logger.info(
        'expeditions with realtime {} of {} ( {:.2f} %)'.format(is_realtime_counter, len(trip_id_list), percentage))


@app.command()
def process_all():
    download_routemanager_file()
    download_predictor_file()

    routemanager_file_path = Path(os.path.join(INPUT_PATH, 'routemanager.proto'))
    predictor_file_path = Path(os.path.join(INPUT_PATH, 'predictor.proto'))

    trip_id_list = read_routemanager_data(routemanager_file_path)
    check_trip_id_is_realtime(trip_id_list)
    # read_predictor_data(predictor_file_path, [381])


if __name__ == "__main__":
    log_file_path = os.path.join(OUTPUT_PATH,
                                 'output.log.{}'.format(datetime.datetime.now().strftime('%y_%m_%d_%H_%M_%S')))
    if Path(log_file_path).exists():
        os.remove(log_file_path)
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s %(levelname)s %(message)s',
        handlers=[
            logging.FileHandler(log_file_path),
            logging.StreamHandler()
        ]
    )
    app()
