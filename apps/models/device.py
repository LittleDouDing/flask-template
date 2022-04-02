from apps.models.models import DeviceAccount
from apps.models import db
from apps.models.general import search_data, handle_modify_info
import re

# from apps.models.models import conn_database
# session = conn_database()

session = db.session


class DeviceManage:
    def __init__(self, datadict, handle_type):
        self._datadict = datadict
        if handle_type == 'add_device_account':
            self.data = self._add_device_account()
        if handle_type == 'modify_device_account':
            self.data = self._modify_device_account()
        if handle_type == 'delete_device_account':
            self.data = self._delete_device_account()
        if handle_type == 'search_device_account':
            self.data = self._search_device_account()

    def _add_device_account(self):
        if not session.query(DeviceAccount).filter_by(full_name=self._datadict.get('full_name')).first():
            try:
                device = DeviceAccount(
                    full_name=self._datadict.get('full_name'),
                    device_type=self._datadict.get('device_type'),
                    place=self._datadict.get('place'),
                    device_name=self._datadict.get('device_name'),
                    manage_ip=self._datadict.get('manage_ip'),
                    room_name=self._datadict.get('room_name'),
                    manufacture=self._datadict.get('manufacture'),
                    remark=self._datadict.get('remark'),
                    register_port=self._datadict.get('register_port'),
                    band_port=self._datadict.get('band_port'),
                    iptv_port=self._datadict.get('iptv_port'),
                    loop_port=self._datadict.get('loop_port'),
                )
                session.add(device)
                session.commit()
                return {'message': 'The device added successfully', 'result': True}
            except Exception as e:
                session.rollback()
                return {'message': re.findall(r'.+"(.+)"', str(e))[0], 'result': False}
        return {'message': 'The device ledger already exists', 'result': False}

    def _modify_device_account(self):
        return handle_modify_info(DeviceAccount, self._datadict, key='device_id')

    def _delete_device_account(self):
        if session.query(DeviceAccount).filter_by(device_id=self._datadict.get('device_id')).first():
            try:
                session.query(DeviceAccount).filter_by(device_id=self._datadict.get('device_id')).delete()
                session.commit()
                return {'message': 'The device account has been successfully deleted', 'result': True}
            except Exception as e:
                session.rollback()
                return {'message': re.findall(r'.+"(.+)"', str(e))[0], 'result': False}
        return {'message': 'The current equipment ledger does not exist', 'result': False}

    def _search_device_account(self):
        page, all_page, results = search_data(table=DeviceAccount, datadict=self._datadict)
        all_device = []
        if results:
            for account in results:
                data = {
                    'device_id': account.device_id,
                    'full_name': account.full_name,
                    'device_type': account.device_type,
                    'place': account.place,
                    'device_name': account.device_name,
                    'manage_ip': account.manage_ip,
                    'room_name': account.room_name,
                    'manufacture': account.manufacture,
                    'remark': account.remark,
                    'register_port': account.register_port,
                    'band_port': account.band_port,
                    'iptv_port': account.iptv_port,
                    'loop_port': account.loop_port,
                }
                all_device.append(data)
            result = {'current_page': page, 'all_page': all_page, 'devices': all_device}
            return {'message': 'success', 'result': True, 'data': result}
        return {'message': 'There are currently no device account', 'result': False}
