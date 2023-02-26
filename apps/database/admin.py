from apps.models.models import User
from apps.models import db
from apps.utils.database_tool import handle_search_info, handle_modify_info, handle_change_password, \
    handle_delete_info, handle_add_info, handle_users_num

session = db.session


class AdminManager:
    def __init__(self, handle_type, datadict=None):
        self._datadict = datadict
        if handle_type == 'change_user_password':
            self.data = self._change_user_password()
        elif handle_type == 'delete_user':
            self.data = self._delete_user()
        elif handle_type == 'add_user':
            self.data = self._add_user()
        elif handle_type == 'modify_user_info':
            self.data = self._modify_user_info()
        elif handle_type == 'get_all_users':
            self.data = self._get_all_users()
        elif handle_type == 'get_users_num':
            self.data = self._get_users_num()

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

    @staticmethod
    def _get_users_num():
        return handle_users_num(User)
