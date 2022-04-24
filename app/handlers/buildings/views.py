from flask import Blueprint

from app.handlers.buildings.serializers import BuildingResponseSerializer

from app.main import CONFIG
from app.utils.response_formatting import response

BUILDINGS_BLUEPRINT = Blueprint('building', __name__)


@BUILDINGS_BLUEPRINT.route("/buildings", methods=['GET'])
def get_buildings():
    service = CONFIG.BUILDING_SERVICE
    serializer = BuildingResponseSerializer()

    instances = service.fetch_all(sort_='country')

    result = serializer.dump({
        'total_count': len(instances),
        'instances': instances
    })

    return response(result)
