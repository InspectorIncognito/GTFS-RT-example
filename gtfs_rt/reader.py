import logging

from google.transit import gtfs_realtime_pb2

logger = logging.getLogger(__name__)


def get_gtfs_rt_entities(proto_file_path):
    """ Read and print content of gtfs-rt file """
    try:
        with open(proto_file_path, "rb") as f:
            feed = gtfs_realtime_pb2.FeedMessage()
            feed.ParseFromString(f.read())

            entities = []
            for entity in feed.entity:
                entities.append(entity)

            logger.info('{} entities in file'.format(len(entities)))

        return entities
    except IOError:
        logger.error('vehicle position' + ": Could not open file.  Creating a new one.")
