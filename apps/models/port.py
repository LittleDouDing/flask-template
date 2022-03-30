from apps.models.models import DevicePort, DeviceAccount
from apps.models import db
from apps.models.general import search_data
from apps.validates import Config
import xlrd
import re

session = db.session


class PortManage:
    def __init__(self, datadict, handle_type):
        self._datadict = datadict
        if handle_type == 'add_port':
            self.data = self._add_port()
        if handle_type == 'get_port':
            self.data = self._get_port()
        if handle_type == 'delete_port':
            self.data = self._delete_port()

    def _add_port(self):
        excel_file = xlrd.open_workbook(file_contents=self._datadict.get('file'))
        t = excel_file.sheet_by_index(0)
        device_data = set([(t.row_values(i)[0], t.row_values(i)[1], t.row_values(i)[2]) for i in range(1, t.nrows)])
        for x in device_data:
            if not session.query(DeviceAccount).filter_by(full_name=x[0].strip(), device_name=x[1].strip(),
                                                          device_type=x[2].strip()).first():
                return {'message': 'The ' + str(x) + ' cannot be queried or the data is incorrect', 'result': False}
        device_ports = {item: [] for item in device_data}
        for i in range(1, t.nrows):
            if re.search(Config.port_regex(), t.row_values(i)[3]):
                device_ports[(t.row_values(i)[0], t.row_values(i)[1], t.row_values(i)[2])].append(t.row_values(i)[3])
            else:
                return {'message': 'The port format is incorrect in row ' + str(i) + ' of the table', 'result': False}
        try:
            data = [DevicePort(full_name=k[0].strip(), device_name=k[1].strip(), device_type=k[2].strip(),
                               ports=list(set(device_ports[k]))) for k in device_ports]
            session.add_all(data)
            session.commit()
            return {'message': 'The device port added successfully', 'result': True}
        except Exception as e:
            session.rollback()
            return {'message': re.findall(r'.+"(.+)"', str(e))[0], 'result': False}

    def _get_port(self):
        page, all_page, results = search_data(table=DevicePort, datadict=self._datadict)
        all_port = []
        if results:
            for item in results:
                data = {
                    'device_name': item.device_name,
                    'full_name': item.full_name,
                    'device_type': item.device_type,
                    'ports': item.ports,
                    'port_id': item.port_id
                }
                all_port.append(data)
            result = {'current_page': page, 'all_page': all_page, 'ports': all_port}
            return {'message': 'success', 'result': True, 'data': result}
        return {'message': 'There are currently no device port', 'result': False}

    def _delete_port(self):
        if session.query(DevicePort).filter_by(port_id=self._datadict.get('port_id')).first():
            try:
                session.query(DevicePort).filter_by(port_id=self._datadict.get('port_id')).delete()
                session.commit()
                return {'message': 'The device port has been successfully deleted', 'result': True}
            except Exception as e:
                session.rollback()
                return {'message': re.findall(r'.+"(.+)"', str(e))[0], 'result': False}
        return {'message': 'The current device port does not exist', 'result': False}
