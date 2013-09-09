# -*- coding: UTF-8 -*-

import json
import requests
from xivo_lettuce.restapi.config import get_config_value
from xivo_lettuce.remote_py_cmd import remote_exec

AUTOPROV_URL = 'https://%s/xivo/configuration/json.php/restricted/provisioning/autoprov?act=configure'
HEADERS = {'Content-Type': 'application/json'}


def provision_device_using_webi(provcode, device_ip):
    hostname = get_config_value('xivo', 'hostname')
    data = json.dumps({'code': provcode, 'ip': device_ip})
    requests.post(url=AUTOPROV_URL % hostname,
                  headers=HEADERS,
                  auth=_prepare_auth(),
                  data=data,
                  verify=False)


def _prepare_auth():
    username = get_config_value('webservices_infos', 'login')
    password = get_config_value('webservices_infos', 'password')

    auth = requests.auth.HTTPBasicAuth(username, password)
    return auth


def delete_all():
    remote_exec(_delete_all)


def _delete_all(channel):
    from xivo_dao.helpers import provd_connector
    config_manager = provd_connector.config_manager()
    device_manager = provd_connector.device_manager()

    for device in device_manager.find():
        try:
            config_manager.remove(device['id'])
        except Exception:
            pass
        device_manager.remove(device['id'])


def create_device(deviceinfo):
    remote_exec(_create_device, deviceinfo=deviceinfo)


def _create_device(channel, deviceinfo):
    from xivo_dao.data_handler.device import services as device_services
    from xivo_dao.data_handler.device.model import Device

    if 'template_id' not in deviceinfo:
        deviceinfo['template_id'] = 'defaultconfigdevice'

    device = Device(**deviceinfo)
    device_services.create(device)


def create_dummy_devices(nb_devices):
    remote_exec(_create_dummy_devices, nb_devices=nb_devices)


def _create_dummy_devices(channel, nb_devices):
    from xivo_dao.data_handler.device import services as device_services
    from xivo_dao.data_handler.device.model import Device

    for i in range(nb_devices):
        device_services.create(Device())
