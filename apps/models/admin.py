from apps.models.models import User, Admin
from apps.models import db
from apps.models.common import handle_search_info, handle_modify_info, handle_change_password, handle_delete_info, \
    handle_add_info
from apps.utils.util_tool import get_table_keys
import re

# from apps.models.models import conn_database
# session = conn_database()

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
        if handle_type == 'check_admin':
            self.data = self._check_admin()

    def _add_user(self):
        return handle_add_info(User, self._datadict, key='username')

    def _delete_user(self):
        return handle_delete_info(User, self._datadict, key='username')

    def _modify_user_info(self):
        return handle_modify_info(User, self._datadict, key='username')

    def _get_all_users(self):
        return handle_search_info(User, self._datadict)

    def _change_user_password(self):
        if session.query(User).filter_by(username=self._datadict.get('username')).first():
            username, new_pwd = self._datadict.get('username'), self._datadict.get('password')
            return handle_change_password(User, new_pwd, condition={'username': username})
        return {'message': 'The current user does not exist', 'result': False}

    def _check_admin(self):
        if session.query(Admin).filter_by(username=self._datadict.get('username')).first():
            return {'message': 'The current user is a legitimate user', 'result': True}
        return {'message': 'The current user is an illegal user', 'result': False}
