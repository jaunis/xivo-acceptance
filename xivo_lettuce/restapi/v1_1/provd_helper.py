# -*- coding: UTF-8 -*-


from xivo_lettuce.remote_py_cmd import remote_exec, remote_exec_with_result


def total_devices():
    return remote_exec_with_result(_total_devices)


def _total_devices(channel):
    from xivo_dao.helpers import provd_connector

    device_manager = provd_connector.device_manager()
    total = len(device_manager.find())
    channel.send(total)


def device_config_has_properties(device_id, properties):
    remote_exec(_device_config_has_properties, device_id=device_id, properties=dict(properties[0]))


def _device_config_has_properties(channel, device_id, properties):
    from xivo_dao.helpers import provd_connector

    provd_config_manager = provd_connector.config_manager()
    provd_device_manager = provd_connector.device_manager()
    device = provd_device_manager.get(device_id)
    if 'config' in device:
        config = provd_config_manager.get(device['config'])
        sip_lines = config['raw_config']['sip_lines']

        sip_line = sip_lines['1']

        keys = [u'username', u'auth_username', u'display_name', u'password', u'number']
        for key in keys:
            if key in properties:
                message = u"Invalid %s ('%s' instead of '%s')" % (key, sip_line[key], properties[key])
                message = message.encode('utf8')
                assert sip_line[key] == properties[key], message
    else:
        assert False, 'Device has no config key.'


def add_or_replace_device_template(properties):
    remote_exec(_add_or_replace_device_template, properties=dict(properties))


def _add_or_replace_device_template(channel, properties):
    from xivo_dao.helpers import provd_connector
    config_manager = provd_connector.config_manager()

    if 'id' in properties:
        existing = config_manager.find({'X_type': 'device', 'id': properties['id']})
        if len(existing) > 0:
            return

    default_properties = {
        'X_type': 'device',
        'deletable': True,
        'parent_ids': [],
        'raw_config': {}
    }

    properties.update(default_properties)

    config_manager.add(properties)


def delete_device(device_id):
    remote_exec(_delete_device, device_id=device_id)


def _delete_device(channel, device_id):
    from xivo_dao.helpers import provd_connector
    config_manager = provd_connector.config_manager()
    device_manager = provd_connector.device_manager()

    try:
        config_manager.remove(device_id)
    except Exception:
        pass
    try:
        device_manager.remove(device_id)
    except Exception:
        pass


def delete_device_with_mac(mac):
    remote_exec(_delete_device_with_mac, mac=mac)


def _delete_device_with_mac(channel, mac):
    from xivo_dao.helpers import provd_connector
    config_manager = provd_connector.config_manager()
    device_manager = provd_connector.device_manager()

    for device in device_manager.find({'mac': mac}):
        try:
            config_manager.remove(device['id'])
        except Exception:
            pass
        device_manager.remove(device['id'])


def remove_devices_over(max_devices):
    remote_exec(_remove_devices_over, max_devices=max_devices)


def _remove_devices_over(channel, max_devices):
    from xivo_dao.helpers import provd_connector
    config_manager = provd_connector.config_manager()
    device_manager = provd_connector.device_manager()

    all_devices = device_manager.find()
    extra_devices = all_devices[max_devices:]

    for device in extra_devices:
        device_manager.remove(device['id'])
        if 'config' in device:
            config_manager.remove(device['id'])


def find_by_mac(mac):
    return remote_exec_with_result(_find_by_mac, mac=mac)


def _find_by_mac(channel, mac):
    from xivo_dao.helpers import provd_connector
    device_manager = provd_connector.device_manager()

    devices = device_manager.find({'mac': mac})
    if len(devices) == 0:
        channel.send(None)
    else:
        channel.send(devices[0])
