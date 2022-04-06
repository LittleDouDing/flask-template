from apps.models.models import DevicePort, DeviceAccount
from apps.models import db
from apps.models.common import handle_search_info, handle_delete_info
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
            self.data = self._get_ports()
        if handle_type == 'delete_port':
            self.data = self._delete_port()

    def _add_port(self):
        excel_file = xlrd.open_workbook(file_contents=self._datadict.get('file'))
        t = excel_file.sheet_by_index(0)
        fix_h, h = ['设备全称', '设备名称', '设备类型', '设备端口'], [t.row_values(0)[i].strip() for i in range(4)]
        if h[0] != fix_h[0] or h[1] != fix_h[1] or h[2] != fix_h[2] or h[3] != fix_h[3]:
            return {'message': 'The first row of the excel table does not meet the specifications', 'result': False}
        device_data = set([(t.row_values(i)[0], t.row_values(i)[1], t.row_values(i)[2]) for i in range(1, t.nrows)])
        for x in device_data:
            if not session.query(DeviceAccount).filter_by(full_name=x[0].strip()).first():
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

    def _get_ports(self):
        return handle_search_info(DevicePort, self._datadict)

    def _delete_port(self):
        return handle_delete_info(DevicePort, self._datadict, 'port_id')
