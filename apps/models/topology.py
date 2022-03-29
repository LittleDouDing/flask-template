from apps.models.models import DeviceTopology, DevicePort
from apps.models import db
import re
import json

session = db.session


class TopologyManage:
    def __init__(self, datadict, handle_type=None):
        self._datadict = datadict
        if handle_type == 'search_device_port':
            self.data = self._search_device_port()
        if handle_type == 'add_topology':
            self.data = self._add_topology()

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

    def _add_topology(self):
        print(self._datadict.get('topology'))
        print(session.query(DeviceTopology).filter_by(topology=json.dumps(self._datadict.get('topology'))).first())
        if not session.query(DeviceTopology).filter(DeviceTopology.topology==self._datadict.get('topology')).first():
            try:
                topology = DeviceTopology(topology=self._datadict.get('topology'))
                session.add(topology)
                # session.commit()
                return {'message': 'The topology was added successfully', 'result': True}
            except Exception as e:
                session.rollback()
                print(e)
                return {'message': re.findall(r'.+"(.+)"', str(e)), 'result': False}
        return {'message': 'The topology already exists', 'result': False}
