from apps.models.models import DeviceTopology, User, Admin
from apps.models import db
import flask_excel as excel
from apps.utils.util_tool import get_table_keys, get_database_err
import xlrd

session = db.session
not_contain_keys = ['device_id', 'port_id', 'topology_id', 'network_id', 'multiple_id']


def handle_search_info(table, datadict):
    page = int(datadict.get('page')) if datadict.get('page') else 1
    conditions = (table.__dict__.get(k).like('%' + datadict.get(k) + '%') for k in list(datadict) if k != 'page')
    results = session.query(table).filter(*conditions).paginate(page=page, per_page=20, error_out=False).items
    count = session.query(table).count()
    all_page = count // 20 if count % 20 == 0 else count // 20 + 1
    if results:
        table_keys = get_table_keys(table, not_contain_keys=['password'])
        all_result = [{key: getattr(obj, key) for key in table_keys} for obj in results]
        all_data = {'current_page': page, 'all_page': all_page, 'results': all_result}
        return {'message': 'success', 'result': True, 'data': all_data}
    return {'message': 'There are currently no record exist', 'result': False}


def handle_modify_info(table, datadict, key):
    from apps.utils.route_tool import check_topology
    obj = session.query(table).filter(getattr(table, key) == datadict.get(key)).first()
    if not obj:
        return {'message': 'The current record does not exist', 'result': False}
    try:
        data = {k: obj.__dict__.get(k) for k in obj.__dict__ if k != '_sa_instance_state'}
        if table == DeviceTopology:
            result = check_topology(datadict.get('topology'))
            if not result.get('result'):
                return {'message': result.get('message'), 'result': False}
            if datadict.get('topology') == data.get('topology'):
                return {'message': 'There is currently no need to modify any information', 'result': False}
        else:
            if len(datadict) <= 1 or set(datadict.items()).issubset(set(data.items())):
                return {'message': 'There is currently no need to modify any information', 'result': False}
        for k in datadict:
            setattr(obj, k, str(datadict.get(k)).replace("'", '"'))
        session.commit()
        return {'message': 'The information modified successfully', 'result': True}
    except Exception as e:
        session.rollback()
        return {'message': get_database_err(e), 'result': False}


def handle_change_password(table, datadict, identity):
    username = datadict.get('username')
    try:
        if identity == 'admin':
            new_pwd = datadict.get('password')
            if not session.query(table).filter_by(username=username).first():
                return {'message': 'The current user does not exist', 'result': False}
            session.query(table).filter_by(username=username).update({table.password: new_pwd})
        if identity == 'user':
            pwd, new_pwd = datadict.get('password'), datadict.get('new_password')
            if not session.query(table).filter_by(username=username, password=pwd).first():
                return {'message': 'The old password you entered is incorrect', 'result': False}
            if pwd == new_pwd:
                return {'message': 'The new password and old password cannot be the same', 'result': False}
            session.query(table).filter_by(username=username).update({table.password: new_pwd})
        session.commit()
        return {'message': 'The password reset successfully', 'result': True}
    except Exception as e:
        session.rollback()
        return {'message': get_database_err(e), 'result': False}


def handle_delete_info(table, datadict, key):
    if session.query(table).filter(getattr(table, key) == datadict.get(key)).first():
        try:
            session.query(table).filter(getattr(table, key) == datadict.get(key)).delete()
            session.commit()
            return {'message': 'The record has been successfully deleted', 'result': True}
        except Exception as e:
            session.rollback()
            return {'message': get_database_err(e), 'result': False}
    return {'message': 'The current record does not exist', 'result': False}


def handle_add_info(table, datadict, keys):
    from apps.utils.route_tool import check_topology
    conditions = (getattr(table, key) == str(datadict.get(key)).replace("'", '"') for key in keys)
    if not session.query(table).filter(*conditions).first():
        try:
            result = check_topology(datadict.get('topology')).get('result') if 'topology' in keys else True
            if not result:
                return {'message': result.get('message'), 'result': False}
            obj = table()
            for k in get_table_keys(table, not_contain_keys=not_contain_keys):
                data = str(datadict.get(k)).replace("'", '"') if k in ['topology', 'ip_address'] else datadict.get(k)
                setattr(obj, k, data)
            session.add(obj)
            session.commit()
            return {'message': 'The record added successfully', 'result': True}
        except Exception as e:
            session.rollback()
            return {'message': get_database_err(e), 'result': False}
    return {'message': 'The current record already exists', 'result': False}


def handle_login(table, datadict):
    username = datadict.get('username')
    password = datadict.get('password')
    user = session.query(table).filter_by(username=username, password=password).first()
    if not user:
        return {'message': 'The user account or password is incorrect', 'result': False}
    author = user.author if table == User else None
    is_admin = True if table == Admin else False
    return {
        'message': 'The current user login successfully', 'result': True, 'author': author, 'is_admin': is_admin
    }


def handle_get_user_info(table, datadict):
    user = session.query(table).filter_by(username=datadict.get('username')).first()
    if user:
        data = {key: getattr(user, key) for key in get_table_keys(table, not_contain_keys=['password'])}
        if table == User:
            data['author'] = user.author
        return {'message': 'success', 'result': True, 'data': data}
    return {'message': 'This user does not exist', 'result': False}


def handle_upload_file(uploaded_file, table, header, require_cols):
    excel_file = xlrd.open_workbook(file_contents=uploaded_file.read())
    sheet = excel_file.sheet_by_index(0)
    temp_header = [str(header).replace('*', '').strip() for header in sheet.row_values(0)]
    if header != temp_header:
        return {'message': 'The first row of the table is different from the template', 'result': False}
    table_keys = get_table_keys(table=table, not_contain_keys=not_contain_keys)
    device_list = []
    try:
        for i in range(1, sheet.nrows):
            device_obj = table()
            for j in range(sheet.ncols):
                if j in require_cols and not sheet.row_values(i)[j]:
                    table_key = ' '.join(table_keys[j].split('_'))
                    return {'message': 'The ' + table_key + ' cant not be empty', 'result': False}
                setattr(device_obj, table_keys[j], str(sheet.row_values(i)[j]).strip())
            device_list.append(device_obj)
        session.add_all(device_list)
        session.commit()
        return {'message': 'All records added successfully', 'result': True}
    except Exception as e:
        return {'message': get_database_err(e), 'result': False}


def handle_export_file(table, header, filename):
    results = session.query(table)
    if not results:
        return {'message': 'There are currently no record exist', 'result': False}
    table_keys = get_table_keys(table, not_contain_keys=not_contain_keys)
    all_result = [header] + [[getattr(obj, key) for key in table_keys] for obj in results]
    data = excel.make_response_from_array(all_result, "xlsx", file_name=filename)
    return {'message': 'success', 'result': True, 'data': data}


def handle_search_topology(datadict):
    from apps.utils.route_tool import get_topology, get_device_ip
    result = handle_search_info(DeviceTopology, {'topology': datadict.get('device_name')})
    data = result.get('data')
    if data:
        results = data.get('results')
        for idx, res in enumerate(results):
            topology_list = eval(res.get('topology'))
            result['data']['results'][idx]['topology_list'] = topology_list
            result['data']['results'][idx]['topology'] = get_topology(res)
            result['data']['results'][idx]['device_ip'] = get_device_ip(topology_list)
    return result
