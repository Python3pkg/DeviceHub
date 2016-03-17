from os import path

from eve.io.mongo import MongoJSONEncoder
from flask.ext.cache import Cache

from app.data_layer import DataLayer
from app.geoip_factory import GeoIPFactory
from app.request import RequestSignedJson
from app.security.authentication import RolesAuth
from app.validation import DeviceHubValidator
from .devicehub import Devicehub
import gnupg

this_directory = path.dirname(path.realpath(__file__))
settings_file = path.abspath(path.join(this_directory, '.', 'settings.py'))
app = Devicehub(
    auth=RolesAuth,
    validator=DeviceHubValidator,
    settings=settings_file,
    static_url_path='/static',
    data=DataLayer
)
app.json_encoder = MongoJSONEncoder
app.request_class = RequestSignedJson
app.gpg = gnupg.GPG()
cache = Cache(app, config={'CACHE_TYPE': 'simple'})
app.geoip = GeoIPFactory()

from hooks import event_hooks

event_hooks(app)

# noinspection PyUnresolvedReferences
from app import error_handler
# noinspection PyUnresolvedReferences
from app.account.login.settings import login
# noinspection PyUnresolvedReferences
from app.static import send_device_icon
# noinspection PyUnresolvedReferences
from app.aggregation.settings import aggregate_view
