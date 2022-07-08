from apps.models.models import DeviceTopology
from apps.models import db
from apps.utils.database_tool import handle_add_info
from apps.utils.database_tool import handle_modify_info, handle_delete_info, handle_search_topology, handle_upload_file, \
    handle_export_file, handle_get_topology

session = db.session


class TopologyManage:
    def __init__(self, upload_file=None, datadict=None, handle_type=None):
        self._datadict = datadict
        self.upload_file = upload_file
        if handle_type == 'import_topology':
            self.data = self._import_topology()
        if handle_type == 'search_topology':
            self.data = self._search_topology()
        if handle_type == 'modify_topology':
            self.data = self._modify_topology()
        if handle_type == 'add_topology':
            self.data = self._add_topology()
        if handle_type == 'delete_topology':
            self.data = self._delete_topology()
        if handle_type == 'export_topology':
            self.data = self._export_topology()
        if handle_type == 'get_topology':
            self.data = self._get_topology()

    def _get_topology(self):
        return handle_get_topology(self._datadict)

    def _import_topology(self):
        return handle_upload_file(self.upload_file, DeviceTopology)

    @staticmethod
    def _export_topology():
        return handle_export_file(DeviceTopology, filename='网络拓扑信息')

    def _search_topology(self):
        return handle_search_topology(self._datadict)

    def _add_topology(self):
        return handle_add_info(DeviceTopology, self._datadict, keys=['topology'])

    def _modify_topology(self):
        return handle_modify_info(DeviceTopology, self._datadict, key='topology_id')

    def _delete_topology(self):
        return handle_delete_info(DeviceTopology, self._datadict, key='topology_id')
