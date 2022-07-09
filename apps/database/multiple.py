from apps.models.models import MultipleAccount, NetworkAccount
from apps.models import db
from apps.utils.database_tool import handle_search_account, handle_modify_info, handle_delete_info, \
    handle_add_info, handle_upload_file, handle_export_file

session = db.session
HEADER = ['区域', '多元化名称', '宽带业务VLAN', 'IPTV业务VLAN', '语音VLAN', '网管VLAN', 'OLT网管IP地址', '主用方式',
          '主用网络拓扑', '主用接入端信息', '主用相关设备IP地址', '备用网管IP地址', '备用网管VLAN', '备用方式', '备用网络拓扑',
          '备用接入端信息', '备用相关设备IP地址', '切换方式', '备注', '调单号', '电路编号', 'OLT应用场景', '上联交换机/分组是否有保护',
          'OLT与交换机/分组是否同机房', '上联交换机/分组设备名称', '经纬度', '开通时间']


class MultipleManage:
    def __init__(self, upload_file=None, datadict=None, handle_type=None):
        self._datadict = datadict
        self.upload_file = upload_file
        if handle_type == 'add_multiple_account':
            self.data = self._add_multiple_account()
        if handle_type == 'modify_multiple_account':
            self.data = self._modify_multiple_account()
        if handle_type == 'delete_multiple_account':
            self.data = self._delete_multiple_account()
        if handle_type == 'search_multiple_account':
            self.data = self._search_multiple_account()
        if handle_type == 'export_multiple_account':
            self.data = self._export_multiple_account()
        if handle_type == 'import_multiple_account':
            self.data = self._import_multiple_account()

    def _add_multiple_account(self):
        return handle_add_info(MultipleAccount, self._datadict, keys=['multiple_name'])

    def _modify_multiple_account(self):
        key = 'multiple_id'
        obj = session.query(MultipleAccount).filter(getattr(MultipleAccount, key) == self._datadict.get(key)).first()
        main_topology, main_access, main_devices = '', '', ''
        topology, access_information = self._datadict.get('main_topology'), self._datadict.get('main_access'),
        relate_device = self._datadict.get('main_devices')
        if obj:
            main_topology = obj.main_topology
            main_access = obj.main_access
            main_devices = obj.main_devices
        result = handle_modify_info(MultipleAccount, self._datadict, key='multiple_id')
        if result.get('result') and topology and access_information and relate_device:
            session.query(NetworkAccount).filter_by(
                topology=main_topology, access_information=main_access, relate_device=main_devices
            ).update({
                NetworkAccount.topology: topology,
                NetworkAccount.access_information: access_information,
                NetworkAccount.relate_device: relate_device
            })
            session.commit()
        return result

    def _delete_multiple_account(self):
        return handle_delete_info(MultipleAccount, self._datadict, key='multiple_id')

    def _search_multiple_account(self):
        return handle_search_account(MultipleAccount, self._datadict)

    def _import_multiple_account(self):
        require_cols = [0, 1, 5, 6, 7, 8, 9, 10, 21, 22, 23, 24]
        return handle_upload_file(self.upload_file, MultipleAccount, header=HEADER, require_cols=require_cols)

    @staticmethod
    def _export_multiple_account():
        return handle_export_file(MultipleAccount, filename='多元化台账信息', header=HEADER)
