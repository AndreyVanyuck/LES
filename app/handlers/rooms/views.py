from flask import Blueprint

from app.handlers.rooms.serializers import RoomResponseSerializer

from app.main import CONFIG
from app.utils.response_formatting import response

ROOMS_BLUEPRINT = Blueprint('room', __name__)


@ROOMS_BLUEPRINT.route("/rooms", methods=['GET'])
def get_rooms():
    service = CONFIG.ROOM_SERVICE
    serializer = RoomResponseSerializer()

    instances = service.fetch_all(sort_='room')

    serializer.context = {
        'buildings': CONFIG.BUILDING_SERVICE.fetch_all(
            in_and_={'id': list({_.building_id for _ in instances})}
        )
    }

    result = serializer.dump({
        'total_count': len(instances),
        'instances': instances
    })

    return response(result)
