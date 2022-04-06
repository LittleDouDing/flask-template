import asyncio
from apps.models.models import User, Admin
from apps.models import db
from apps.models import get_value, set_value
from apps.models.common import handle_change_password, handle_modify_info
from apps.utils.util_tool import get_table_keys

# from apps.models.models import conn_database
# session = conn_database()

session = db.session


class UserManager:
    def __init__(self, datadict, handle_type, usertype='user'):
        self._datadict = datadict
        self._table = Admin if usertype == 'admin' else User
        if handle_type == 'modify_password':
            self.data = self._change_password()
        if handle_type == 'user_login':
            self.data = self._user_login()
        if handle_type == 'get_info':
            self.data = self._get_userinfo()
        if handle_type == 'modify_info':
            self.data = self._modify_information()
        if handle_type == 'get_author':
            self.author = self._get_author()

    def _get_userinfo(self):
        user = session.query(self._table).filter_by(username=self._datadict.get('username')).first()
        if user:
            data = {key: getattr(user, key) for key in get_table_keys(self._table, not_contain_keys=['password'])}
            if self._table == User:
                data['author'] = user.author
            return {'message': 'success', 'result': True, 'data': data}
        return {'message': 'This user does not exist', 'result': False}

    def _user_login(self):
        username = self._datadict.get('username')
        password = self._datadict.get('password')
        user = session.query(self._table).filter_by(username=username, password=password).first()
        if not user:
            return {'message': 'The user account or password is incorrect', 'result': False}
        return {'message': 'The current user login successfully', 'result': True}

    def _change_password(self):
        old_pwd, new_pwd = self._datadict.get('password'), self._datadict.get('new_password')
        username = self._datadict.get('username')
        data = self._user_login()
        if self._table == Admin:
            if not session.query(self._table).filter_by(username=username).first():
                return {'message': 'The current user does not exist', 'result': False}
            if data.get('result'):
                return {'message': 'The new password and old password cannot be the same', 'result': False}
        if self._table == User and not data.get('result'):
            return data
        if old_pwd != new_pwd:
            return handle_change_password(self._table, new_pwd, condition={'username': username, 'password': old_pwd})
        return {'message': 'The new password and old password cannot be the same', 'result': False}

    def _modify_information(self):
        return handle_modify_info(self._table, self._datadict, key='username')

    def _get_author(self):
        author = asyncio.run(get_value(self._datadict.get('username') + '_author'))
        if author:
            return author
        user = session.query(User).filter_by(username=self._datadict.get('username')).first()
        asyncio.run(set_value(self._datadict.get('username') + '_author', user.author, expire=1800))
        return user.author



