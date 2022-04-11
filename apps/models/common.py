from apps.models.models import DeviceTopology
from apps.models import db
import re

session = db.session


def handle_search_info(table, datadict):
    from apps.utils.util_tool import get_table_keys
    page = int(datadict.get('page')) if datadict.get('page') else 1
    conditions = (table.__dict__.get(k).like('%' + datadict.get(k) + '%') for k in list(datadict) if k != 'page')
    results = session.query(table).filter(*conditions).paginate(page=page, per_page=20, error_out=False).items
    count = session.query(table).count()
    all_page = count // 20 if count % 20 == 0 else count // 20 + 1
    if results:
        not_contain_keys = ['device_account', 'device_account1', 'device_account2', 'password']
        table_keys = get_table_keys(table, not_contain_keys=not_contain_keys)
        all_result = [{key: getattr(obj, key) for key in table_keys} for obj in results]
        all_data = {'current_page': page, 'all_page': all_page, 'results': all_result}
        return {'message': 'success', 'result': True, 'data': all_data}
    return {'message': 'There are currently no record exist', 'result': False}


def handle_modify_info(table, datadict, key):
    obj = session.query(table).filter(getattr(table, key) == datadict.get(key)).first()
    if not obj:
        return {'message': 'The current record does not exist', 'result': False}
    try:
        data = {k: obj.__dict__.get(k) for k in obj.__dict__ if k != '_sa_instance_state'}
        if table == DeviceTopology:
            if datadict.get('topology') == data.get('topology'):
                return {'message': 'There is currently no need to modify any information', 'result': False}
        else:
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


def handle_delete_info(table, datadict, key):
    if session.query(table).filter(getattr(table, key) == datadict.get(key)).first():
        try:
            session.query(table).filter(getattr(table, key) == datadict.get(key)).delete()
            session.commit()
            return {'message': 'The record has been successfully deleted', 'result': True}
        except Exception as e:
            session.rollback()
            return {'message': re.findall(r'.+"(.+)"', str(e))[0], 'result': False}
    return {'message': 'The current record does not exist', 'result': False}


def handle_add_info(table, datadict, key):
    if table != DeviceTopology:
        result = session.query(table).filter(getattr(table, key) == datadict.get(key)).first()
    else:
        result = datadict.get(key) in [x.topology for x in session.query(DeviceTopology).all()]
    if not result:
        try:
            obj = table()
            not_contain_keys = ['device_id', 'port_id', 'topology_id', 'network_id', 'multiple_id']
            from apps.utils.util_tool import get_table_keys
            for key in get_table_keys(table, not_contain_keys=not_contain_keys):
                setattr(obj, key, datadict.get(key))
            session.add(obj)
            session.commit()
            return {'message': 'The record added successfully', 'result': True}
        except Exception as e:
            session.rollback()
            return {'message': re.findall(r'.+"(.+)"', str(e))[0], 'result': False}
    return {'message': 'The current record already exists', 'result': False}
