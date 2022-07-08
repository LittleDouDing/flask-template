from apps.models.models import DeviceAccount
from apps.models import db
from apps.utils.database_tool import handle_search_info, handle_modify_info, handle_delete_info, handle_add_info, \
    handle_upload_file, handle_export_file

session = db.session
HEADER = ['区域', '地点', '设备名称', '设备别名', '管理IP', '网络层次', '厂商', '设备类型', '设备型号', '设备所在位置', '备注信息']


class DeviceManage:
    def __init__(self, upload_file=None, datadict=None, handle_type=None):
        self._datadict = datadict
        self.upload_file = upload_file
        if handle_type == 'add_device_account':
            self.data = self._add_device_account()
        if handle_type == 'modify_device_account':
            self.data = self._modify_device_account()
        if handle_type == 'delete_device_account':
            self.data = self._delete_device_account()
        if handle_type == 'search_device_account':
            self.data = self._search_device_account()
        if handle_type == 'import_device_account':
            self.data = self._import_device_account()
        if handle_type == 'export_device_account':
            self.data = self._export_device_account()

    def _add_device_account(self):
        return handle_add_info(DeviceAccount, self._datadict, keys=['device_name'])

    def _modify_device_account(self):
        return handle_modify_info(DeviceAccount, self._datadict, key='device_id')

    def _delete_device_account(self):
        return handle_delete_info(DeviceAccount, self._datadict, key='device_id')

    def _search_device_account(self):
        return handle_search_info(DeviceAccount, self._datadict)

    def _import_device_account(self):
        return handle_upload_file(self.upload_file, DeviceAccount, header=HEADER, require_cols=[0, 1, 2, 3, 4])

    @staticmethod
    def _export_device_account():
        return handle_export_file(DeviceAccount, filename='设备台账信息', header=HEADER)
