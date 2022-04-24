from flask import Blueprint

from app.handlers.departments.serializers import DepartmentResponseSerializer

from app.main import CONFIG
from app.utils.response_formatting import response

DEPARTMENTS_BLUEPRINT = Blueprint('department', __name__)


@DEPARTMENTS_BLUEPRINT.route("/departments", methods=['GET'])
def get_departments():
    service = CONFIG.DEPARTMENT_SERVICE
    serializer = DepartmentResponseSerializer()

    instances = service.fetch_all(sort_='name')

    result = serializer.dump({
        'total_count': len(instances),
        'instances': instances
    })

    return response(result)
