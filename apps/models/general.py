import asyncio
from apps.models.models import User, Admin
from apps.models import db
from apps.models import get_value, set_value
import re

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
            data = {
                'username': user.username,
                'name': user.name,
                'sex': user.sex,
                'email': user.email,
                'phone': user.phone,
            }
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
                return {'message': 'New password and old password cannot be the same', 'result': False}
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


def search_data(table, datadict):
    page = int(datadict.get('page')) if datadict.get('page') else 1
    conditions = (table.__dict__.get(k).like('%' + datadict.get(k) + '%') for k in list(datadict) if k != 'page')
    results = session.query(table).filter(*conditions).paginate(page=page, per_page=20, error_out=False).items
    count = session.query(table).count()
    all_page = count // 20 if count % 20 == 0 else count // 20 + 1
    return page, all_page, results


def handle_modify_info(table, datadict, key):
    obj = session.query(table).filter(getattr(table, key) == datadict.get(key)).first()
    if not obj:
        return {'message': 'The current record does not exist', 'result': False}
    try:
        data = {k: obj.__dict__.get(k) for k in obj.__dict__ if k != '_sa_instance_state'}
        if len(datadict) <= 1 or set(datadict.items()).issubset(set(data.items())):
            return {'message': 'There is currently no need to modify any information', 'result': False}
        for k in datadict:
            setattr(obj, k, datadict.get(k))
        session.commit()
        return {'message': 'The information modified successfully', 'result': True}
    except Exception as e:
        session.rollback()
        return {'message': re.findall(r'.+"(.+)"', str(e))[0], 'result': False}


def handle_change_password(table, new_pwd, **kwargs):
    try:
        condition = kwargs.get('condition')
        session.query(table).filter_by(**condition).update({table.password: new_pwd})
        session.commit()
        return {'message': 'The password reset successfully', 'result': True}
    except Exception as e:
        session.rollback()
        return {'message': re.findall(r'.+"(.+)"', str(e))[0], 'result': False}

