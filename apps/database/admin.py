from apps.models.models import User
from apps.models import db
from apps.utils.database_tool import handle_search_info, handle_modify_info, handle_change_password, \
    handle_delete_info, handle_add_info

session = db.session


class AdminManager:
    def __init__(self, datadict, handle_type):
        self._datadict = datadict
        if handle_type == 'change_user_password':
            self.data = self._change_user_password()
        if handle_type == 'delete_user':
            self.data = self._delete_user()
        if handle_type == 'add_user':
            self.data = self._add_user()
        if handle_type == 'modify_user_info':
            self.data = self._modify_user_info()
        if handle_type == 'get_all_users':
            self.data = self._get_all_users()

    def _add_user(self):
        return handle_add_info(User, self._datadict, keys=['username'])

    def _delete_user(self):
        return handle_delete_info(User, self._datadict, key='username')

    def _modify_user_info(self):
        return handle_modify_info(User, self._datadict, key='username')

    def _get_all_users(self):
        return handle_search_info(User, self._datadict)

    def _change_user_password(self):
        return handle_change_password(User, self._datadict, identity='admin')
