import os
import time
import uuid

from google.transit import gtfs_realtime_pb2


def create_vehicle_position_entity(timestamp, trip_route_id, trip_direction_id, vehicle_id, vehicle_label,
                                   vehicle_license_plate, pos_latitude, pos_longitude, pos_bearing, pos_odometer,
                                   pos_speed):
    feed_entity = gtfs_realtime_pb2.FeedEntity()
    # The ids are used only to provide incrementality support. The id should be unique within a FeedMessage. Consequent
    # FeedMessages may contain FeedEntities with the same id. In case of a DIFFERENTIAL update the new FeedEntity with
    # some id will replace the old FeedEntity with the same id (or delete it - see is_deleted below). The actual GTFS
    # entities (e.g. stations, routes, trips) referenced by the feed must be specified by explicit selectors (see
    # EntitySelector below for more info).
    feed_entity.id = str(uuid.uuid4())

    # moment at which the vehicle's position was measured. In POSIX time
    feed_entity.vehicle.timestamp = timestamp

    # trip descriptor
    feed_entity.vehicle.trip.route_id = trip_route_id
    feed_entity.vehicle.trip.direction_id = trip_direction_id

    # vehicle descriptor
    feed_entity.vehicle.vehicle.id = vehicle_id
    feed_entity.vehicle.vehicle.label = vehicle_label
    feed_entity.vehicle.vehicle.license_plate = vehicle_license_plate

    # position
    feed_entity.vehicle.position.latitude = pos_latitude
    feed_entity.vehicle.position.longitude = pos_longitude
    feed_entity.vehicle.position.bearing = pos_bearing
    feed_entity.vehicle.position.odometer = pos_odometer
    feed_entity.vehicle.position.speed = pos_speed

    return feed_entity


def create_feed_message(timestamp=None):
    feed_message = gtfs_realtime_pb2.FeedMessage()
    feed_message.header.gtfs_realtime_version = "2.0"
    # This timestamp identifies the moment when the content of this feed has been created. In POSIX time
    feed_message.header.timestamp = int(time.time()) if timestamp is None else timestamp

    return feed_message


def build_vehicle_location_proto():
    feed_message = create_feed_message()

    for gps in range(2):
        trip_route_id = '506'
        trip_direction_id = 0

        vehicle_id = str(uuid.uuid4())
        vehicle_label = ''
        vehicle_license_plate = 'AABB45'

        timestamp = int(time.time())
        pos_latitude = -33.4361819
        pos_longitude = -70.6573692
        pos_bearing = 1
        pos_odometer = 1
        pos_speed = 0

        vehicle_location = create_vehicle_position_entity(timestamp, trip_route_id, trip_direction_id, vehicle_id,
                                                          vehicle_label, vehicle_license_plate, pos_latitude,
                                                          pos_longitude, pos_bearing, pos_odometer, pos_speed)
        feed_message.entity.append(vehicle_location)

    # Write the new address book back to disk.
    f = open(os.path.join('output', 'data.proto'), "wb")
    f.write(feed_message.SerializeToString())
    f.close()


def read_gtfs_rt():
    # Read the existing gtfs-rt.
    try:
        f = open(os.path.join('output', 'data.proto'), "rb")
        feed = gtfs_realtime_pb2.FeedMessage()
        feed.ParseFromString(f.read())

        for entity in feed.entity:
            if entity.HasField('vehicle'):
                print(entity.vehicle)

        f.close()
    except IOError:
        print('vehicle position' + ": Could not open file.  Creating a new one.")


if __name__ == '__main__':
    build_vehicle_location_proto()
    read_gtfs_rt()
