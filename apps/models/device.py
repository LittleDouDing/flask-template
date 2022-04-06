from apps.models.models import DeviceAccount
from apps.models import db
from apps.models.common import handle_search_info, handle_modify_info, handle_delete_info, handle_add_info

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
        return handle_add_info(DeviceAccount, self._datadict, 'full_name')

    def _modify_device_account(self):
        return handle_modify_info(DeviceAccount, self._datadict, key='device_id')

    def _delete_device_account(self):
        return handle_delete_info(DeviceAccount, self._datadict, key='device_id')

    def _search_device_account(self):
        return handle_search_info(DeviceAccount, self._datadict)
