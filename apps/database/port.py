from apps.models.models import DevicePort
from apps.models import db
from apps.utils.database_tool import handle_search_info, handle_delete_info, handle_add_info, handle_upload_file, \
    handle_export_file, handle_modify_info

session = db.session
HEADER = ['设备名称', '设备别称', '所属区域', '物理带宽', '设备IP', '端口名称', '端口描述']


class PortManage:
    def __init__(self, upload_file=None, datadict=None, handle_type=None):
        self.upload_file = upload_file
        self._datadict = datadict
        if handle_type == 'add_port':
            self.data = self._add_port()
        if handle_type == 'get_port':
            self.data = self._get_ports()
        if handle_type == 'modify_port':
            self.data = self._modify_port()
        if handle_type == 'delete_port':
            self.data = self._delete_port()
        if handle_type == 'import_device_port':
            self.data = self._import_device_port()
        if handle_type == 'export_device_port':
            self.data = self._export_device_port()

    def _add_port(self):
        return handle_add_info(DevicePort, self._datadict, keys=['device_name', 'device_alias', 'manage_ip', 'port'])

    def _get_ports(self):
        return handle_search_info(DevicePort, self._datadict)

    def _modify_port(self):
        return handle_modify_info(DevicePort, self._datadict, key='port_id')

    def _delete_port(self):
        return handle_delete_info(DevicePort, self._datadict, 'port_id')

    def _import_device_port(self):
        return handle_upload_file(self.upload_file, DevicePort, header=HEADER, require_cols=[0, 1, 2, 3, 4, 5])

    @staticmethod
    def _export_device_port():
        return handle_export_file(DevicePort, filename='设备端口信息', header=HEADER)
