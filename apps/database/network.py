from apps.models.models import NetworkAccount
from apps.models import db
from apps.utils.database_tool import handle_search_network_account, handle_modify_info, handle_delete_info, \
    handle_add_info, handle_export_file, handle_upload_file

session = db.session
HEADER = ['区域', '客户名称', '客户VLAN', '客户IP地址', '网关和掩码', '子接口', '交换机网络拓扑', '接入端信息', '相关设备', '带宽',
          '业务类型', '客户地址', '客户联系人', '客户联系电话', '项目经理', '项目经理联系电话', '备注', '竣工时间', '产品号码',
          '调单号', '电路编号', '80端口是否开放']


class NetworkManage:
    def __init__(self, upload_file=None, datadict=None, handle_type=None):
        self._datadict = datadict
        self.upload_file = upload_file
        if handle_type == 'add_network_account':
            self.data = self._add_network_account()
        if handle_type == 'modify_network_account':
            self.data = self._modify_network_account()
        if handle_type == 'delete_network_account':
            self.data = self._delete_network_account()
        if handle_type == 'search_network_account':
            self.data = self._search_network_account()
        if handle_type == 'export_network_account':
            self.data = self._export_network_account()
        if handle_type == 'import_network_account':
            self.data = self._import_network_account()

    def _add_network_account(self):
        return handle_add_info(NetworkAccount, self._datadict, keys=['ip_address'])

    def _modify_network_account(self):
        return handle_modify_info(NetworkAccount, self._datadict, key='network_id')

    def _delete_network_account(self):
        return handle_delete_info(NetworkAccount, self._datadict, key='network_id')

    def _search_network_account(self):
        return handle_search_network_account(NetworkAccount, self._datadict)

    def _import_network_account(self):
        require_cols = [0, 1, 3, 4, 6, 7, 8]
        return handle_upload_file(self.upload_file, NetworkAccount, header=HEADER, require_cols=require_cols)

    @staticmethod
    def _export_network_account():
        return handle_export_file(NetworkAccount, filename='专线台账信息', header=HEADER)
