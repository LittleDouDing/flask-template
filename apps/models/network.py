from apps.models.models import NetworkAccount
from apps.models import db
from apps.models.common import handle_search_info, handle_modify_info, handle_delete_info, handle_add_info

# from apps.models.models import conn_database
# session = conn_database()

session = db.session


class NetworkManage:
    def __init__(self, datadict, handle_type):
        self._datadict = datadict
        if handle_type == 'add_network_account':
            self.data = self._add_network_account()
        if handle_type == 'modify_network_account':
            self.data = self._modify_network_account()
        if handle_type == 'delete_network_account':
            self.data = self._delete_network_account()
        if handle_type == 'search_network_account':
            self.data = self._search_network_account()

    def _add_network_account(self):
        return handle_add_info(NetworkAccount, self._datadict, 'start_ip')

    def _modify_network_account(self):
        return handle_modify_info(NetworkAccount, self._datadict, key='network_id')

    def _delete_network_account(self):
        return handle_delete_info(NetworkAccount, self._datadict, key='network_id')

    def _search_network_account(self):
        return handle_search_info(NetworkAccount, self._datadict)
