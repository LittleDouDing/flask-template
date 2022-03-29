from apps.models.models import User
from apps.models import db
import re

# from apps.models.models import conn_database
# session = conn_database()

session = db.session


class AdminManager:
    def __init__(self, datadict, handle_type=None):
        self._datadict = datadict
        if handle_type == 'change_user_password':
            self.data = self._change_user_password()
        if handle_type == 'delete_user':
            self.data = self._delete_user()
        if handle_type == 'add_user':
            self.data = self._add_user()
        if handle_type == 'modify_user_info':
            self.data = self._modify_user_info()
        if handle_type == 'all_users':
            self.data = self._get_all_users()

    def _add_user(self):
        if not session.query(User).filter_by(username=self._datadict.get('username')).first():
            try:
                user = User(
                    username=self._datadict.get('username'),
                    password=self._datadict.get('password'),
                    author=self._datadict.get('author'),
                    name=self._datadict.get('name'),
                    sex=self._datadict.get('sex'),
                    email=self._datadict.get('email'),
                    phone=self._datadict.get('phone'),
                )
                session.add(user)
                session.commit()
                return {'message': 'The user added successfully', 'result': True}
            except Exception as e:
                session.rollback()
                return {'message': re.findall(r'.+"(.+)"', str(e))[0], 'result': False}
        return {'message': 'The current user already exists, please change the user account', 'result': False}

    def _change_user_password(self):
        if session.query(User).filter_by(username=self._datadict.get('username')).first():
            try:
                username, new_pwd = self._datadict.get('username'), self._datadict.get('password')
                session.query(User).filter_by(username=username).update({User.password: new_pwd})
                session.commit()
                return {'message': 'The user password changed successfully', 'result': True}
            except Exception as e:
                session.rollback()
                return {'message': re.findall(r'.+"(.+)"', str(e))[0], 'result': False}
        return {'message': 'The current user does not exist', 'result': False}

    def _delete_user(self):
        if session.query(User).filter_by(username=self._datadict.get('username')).first():
            try:
                session.query(User).filter_by(username=self._datadict.get('username')).delete()
                session.commit()
                return {'message': 'The user has been successfully deleted', 'result': True}
            except Exception as e:
                session.rollback()
                return {'message': re.findall(r'.+"(.+)"', str(e))[0], 'result': False}
        return {'message': 'The current user does not exist', 'result': False}

    def _modify_user_info(self):
        if session.query(User).filter_by(username=self._datadict.get('username')).first():
            try:
                session.query(User).filter_by(username=self._datadict.get('username')).update({
                    User.name: self._datadict.get('name'),
                    User.sex: self._datadict.get('sex'),
                    User.email: self._datadict.get('email'),
                    User.phone: self._datadict.get('phone'),
                    User.author: self._datadict.get('author'),
                })
                session.commit()
                return {'message': 'The user information modified successfully', 'result': True}
            except Exception as e:
                session.rollback()
                return {'message': re.findall(r'.+"(.+)"', str(e))[0], 'result': False}
        return {'message': 'The current user does not exist', 'result': False}

    def _get_all_users(self):
        current_page = int(self._datadict.get('page')) if self._datadict.get('page') else 1
        users = session.query(User).paginate(page=current_page, per_page=20, error_out=False).items
        all_user = []
        if users:
            for user in users:
                data = {
                    'username': user.username,
                    'name': user.name,
                    'sex': user.sex,
                    'email': user.email,
                    'phone': user.phone,
                    'author': user.author
                }
                all_user.append(data)
            user_count = session.query(User).count()
            all_page = user_count // 20 if user_count % 20 == 0 else user_count // 20 + 1
            all_data = {'current_page': current_page, 'all_page': all_page, 'users': all_user}
            return {'message': 'success', 'result': True, 'data': all_data}
        return {'message': 'There are currently no users', 'result': False}
