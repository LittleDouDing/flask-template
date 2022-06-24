from apps.models.models import DeviceTopology, DevicePort
from apps.models import db
from apps.utils.database_tool import handle_add_info
from apps.utils.database_tool import handle_modify_info, handle_delete_info, handle_search_topology


session = db.session


class TopologyManage:
    def __init__(self, datadict, handle_type):
        self._datadict = datadict
        if handle_type == 'search_device_port':
            self.data = self._search_device_port()
        if handle_type == 'search_topology':
            self.data = self._search_topology()
        if handle_type == 'modify_topology':
            self.data = self._modify_topology()
        if handle_type == 'add_topology':
            self.data = self._add_topology()
        if handle_type == 'delete_topology':
            self.data = self._delete_topology()

    def _search_device_port(self):
        device_name = self._datadict.get('device_name')
        device_type = self._datadict.get('device_type')
        device_port = session.query(DevicePort).filter(DevicePort.device_name.like('%' + device_name + '%'),
                                                       DevicePort.device_type == device_type).first()
        if device_port:
            data = {
                'device_name': device_port.device_name,
                'ports': device_port.ports,
            }
            return {'message': 'success', 'result': True, 'data': data}
        return {'message': 'The device port does not exist', 'result': False}

    def _search_topology(self):
        return handle_search_topology(self._datadict)

    def _add_topology(self):
        return handle_add_info(DeviceTopology, self._datadict, keys=['topology'])

    def _modify_topology(self):
        return handle_modify_info(DeviceTopology, self._datadict, key='topology_id')

    def _delete_topology(self):
        return handle_delete_info(DeviceTopology, self._datadict, key='topology_id')
