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
        if handle_type == 'check_user':
            self.data = self._check_user()
        if handle_type == 'get_info':
            self.data = self._read_userinfo()
        if handle_type == 'modify_info':
            self.data = self._modify_information()
        if handle_type == 'get_author':
            self.author = self._get_author()

    def _read_userinfo(self):
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

    def _check_user(self):
        username = self._datadict.get('username')
        password = self._datadict.get('password')
        user = session.query(self._table).filter_by(username=username, password=password).first()
        if not user:
            return {'message': 'Incorrect user account or password', 'result': False}
        return {'message': 'The current user is a legitimate user', 'result': True}

    def _change_password(self):
        old_pwd, new_pwd = self._datadict.get('password'), self._datadict.get('new_password')
        username = self._datadict.get('username')
        data = self._check_user()
        if self._table == Admin:
            if not session.query(self._table).filter_by(username=username).first():
                return {'message': 'The current user does not exist', 'result': False}
            if data.get('result'):
                return {'message': 'New password and old password cannot be the same', 'result': False}
        if self._table == User and not data.get('result'):
            return data
        if old_pwd != new_pwd:
            try:
                session.query(self._table).filter_by(username=username, password=old_pwd).update(
                    {self._table.password: new_pwd})
                session.commit()
                return {'message': 'Password reset complete', 'result': True}
            except Exception as e:
                session.rollback()
                return {'message': re.findall(r'.+"(.+)"', str(e))[0], 'result': False}
        return {'message': 'New password and old password cannot be the same', 'result': False}

    def _modify_information(self):
        if not session.query(self._table).filter_by(username=self._datadict.get('username')).first():
            return {'message': 'The current user does not exist', 'result': False}
        try:
            user = session.query(self._table).filter_by(username=self._datadict.get('username')).first()
            for key in self._datadict:
                setattr(user, key, self._datadict.get(key))
            session.commit()
            return {'message': 'Information modified successfully', 'result': True}
        except Exception as e:
            session.rollback()
            return {'message': re.findall(r'.+"(.+)"', str(e))[0], 'result': False}

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
