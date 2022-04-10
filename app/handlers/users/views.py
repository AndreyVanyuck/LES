from flask import g, Blueprint

from app.handlers.users.forms import UserForm
from app.main import CONFIG

USER_BLUEPRINT = Blueprint('user', __name__)


@USER_BLUEPRINT.route("/user/create", methods=['POST'])
def create_user():
    form = UserForm().load(g.request_data)

    service = CONFIG.USER_SERVICE
    serializer = CampaignListResponseSerializer()

    if 'external_id_list' in form.keys():
        external_id_list = form.pop('external_id_list')
        form['in_and_'] = {'external_id': [str(_) for _ in external_id_list.split(',')]}

    instances = service.fetch_all(**form)

    serializer.context = {
        'online_metrics': CONFIG.CAMPAIGN_ONLINE_METRICS_SERVICE.fetch(
            in_={'campaign_id': [_.external_id for _ in instances if _.external_id]})
    }
    result = serializer.dump({
        'total_count': service.count(**form),
        'instances': instances
    })

    return response(result)