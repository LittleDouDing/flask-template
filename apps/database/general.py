from apps.models.models import User, Admin
from apps.models import db
from apps.utils.database_tool import handle_change_password, handle_modify_info, handle_login, handle_get_user_info

session = db.session


class UserManager:
    def __init__(self, datadict, handle_type, usertype='user'):
        self._datadict = datadict
        self._table = Admin if usertype == 'admin' else User
        self.identity = usertype
        if handle_type == 'modify_password':
            self.data = self._change_password()
        if handle_type == 'user_login':
            self.data = self._user_login()
        if handle_type == 'get_info':
            self.data = self._get_user_info()
        if handle_type == 'modify_info':
            self.data = self._modify_information()

    def _get_user_info(self):
        return handle_get_user_info(self._table, self._datadict)

    def _user_login(self):
        return handle_login(self._table, self._datadict)

    def _change_password(self):
        return handle_change_password(self._table, self._datadict, identity=self.identity)

    def _modify_information(self):
        return handle_modify_info(self._table, self._datadict, key='username')
