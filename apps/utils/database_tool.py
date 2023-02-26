import asyncio
from apps.models.models import User, Admin
from apps.utils.util_tool import get_table_keys, get_database_err, get_conditions, encrypt_password, \
    check_illegal_data, get_table_id, validate_value
from apps.models import get_value
from apps.models import db
import flask_excel as excel
from datetime import datetime
import xlrd

session = db.session
not_contain_keys = ['device_id', 'port_id', 'topology_id', 'network_id', 'multiple_id']


def handle_search_info(table, datadict):
    page = int(datadict.get('page')) if datadict.get('page') else 1
    limit = int(datadict.get('limit')) if datadict.get('limit') else 10
    datadict = {key: datadict.get(key) for key in datadict if datadict.get(key)}
    conditions = get_conditions(datadict, table)
    tid = get_table_id(table)
    results = session.query(table).order_by(desc(tid)).filter(*conditions).paginate(page=page, per_page=limit,
                                                                                    error_out=False).items
    total = session.query(table).filter(*get_conditions(datadict, table)).count()
    if results:
        table_keys = get_table_keys(table, not_contain_keys=['password'])
        all_result = [{key: getattr(obj, key) for key in table_keys} for obj in results]
        all_data = {'current_page': page, 'total': total, 'results': all_result}
        return {'message': 'success', 'result': True, 'data': all_data}
    return {'message': 'There are currently no record exist', 'result': False}


def handle_modify_info(table, datadict, key):
    obj = session.query(table).filter(getattr(table, key) == datadict.get(key)).first()
    if not obj:
        return {'message': 'The current record does not exist', 'result': False}
    try:
        data = {k: obj.__dict__.get(k) for k in obj.__dict__ if k != '_sa_instance_state'}
        if table == DeviceTopology:
            result = check_topology(eval(datadict.get('topology')))
            if not result.get('result'):
                return {'message': result.get('message'), 'result': False}
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
        return {'message': get_database_err(e), 'result': False}


def handle_delete_info(table, datadict, key):
    ids = [int(item) for item in eval(datadict.get(key))]
    if session.query(table).filter(table.__dict__.get(key).in_(ids)).first():
        try:
            session.query(table).filter(table.__dict__.get(key).in_(ids)).delete()
            session.commit()
            return {'message': 'The record has been successfully deleted', 'result': True}
        except Exception as e:
            session.rollback()
            return {'message': get_database_err(e), 'result': False}
    return {'message': 'The current record does not exist', 'result': False}


def handle_add_info(table, datadict, keys):
    if table == NetworkAccount:
        conditions = get_network_conditions(table, datadict)
    else:
        conditions = (getattr(table, key) == datadict.get(key) for key in keys)
    if not session.query(table).filter(*conditions).first():
        try:
            result = check_topology(eval(datadict.get('topology'))) if 'topology' in keys else {'result': True}
            if not result.get('result'):
                return {'message': result.get('message'), 'result': False}
            obj = table()
            for k in get_table_keys(table, not_contain_keys=not_contain_keys):
                setattr(obj, k, datadict.get(k))
            session.add(obj)
            session.commit()
            return {'message': 'The record added successfully', 'result': True}
        except Exception as e:
            session.rollback()
            return {'message': get_database_err(e), 'result': False}
    return {'message': 'The current record already exists', 'result': False}


def handle_upload_file(uploaded_file, table, header=None):
    try:
        excel_file = xlrd.open_workbook(file_contents=uploaded_file.read())
    except Exception as e:
        return {'message': str(e), 'result': False}
    sheet = excel_file.sheet_by_index(0)
    if table != DeviceTopology and header:
        start_index = 1
        temp_header = [str(header).replace('*', '').strip() for header in sheet.row_values(0)]
        if header != temp_header:
            return {'message': 'The first row of the table is different from the template', 'result': False}
    else:
        start_index = 0
    table_keys = get_table_keys(table=table, not_contain_keys=not_contain_keys)
    obj_list = []
    try:
        validate_results = []
        for i in range(start_index, sheet.nrows):
            obj = table()
            table_list = []
            if table != DeviceTopology:
                for j in range(sheet.ncols):
                    cell_value = sheet.row_values(i)[j]

                    if check_illegal_data(cell_value):
                        line = '(' + str(i + 1) + ' line)'
                        return {'message': 'The ' + cell_value + ' is illegal' + line, 'result': False}
                    if 'time' in table_keys[j]:
                        data = xlrd.xldate_as_datetime(cell_value, 0).date()
                        table_list.append((table_keys[j], str(data)))
                    else:
                        table_list.append((table_keys[j], cell_value))
                        data = str(int(cell_value)) if isinstance(cell_value, float) else str(cell_value).strip()
                    setattr(obj, table_keys[j], data)
                validate_result = validate_value(table_list, table)
                if validate_result:
                    validate_results.append(validate_result + '(' + str(i + 1) + ' line)')
            else:
                for j in range(sheet.ncols):
                    cell_value = sheet.row_values(i)[j]
                    if ':' not in sheet.row_values(i)[j]:
                        return {'message': 'The format of topology ' + cell_value + ' is illegal', 'result': False}
                result = check_topology(sheet.row_values(i))
                if not result.get('result'):
                    return {'message': result.get('message'), 'result': False}
                topology = str([sheet.row_values(i)[j].replace("'", '"').strip() for j in range(sheet.ncols)])
                setattr(obj, 'topology', topology)
            obj_list.append(obj)
        if validate_results:
            return {'message': validate_results, 'result': False}
        session.add_all(obj_list)
        session.commit()
        return {'message': 'All records added successfully', 'result': True}
    except Exception as e:
        session.rollback()
        return {'message': get_database_err(e), 'result': False}


def handle_export_file(table, filename, header=None):
    results = session.query(table)
    if not results:
        return {'message': 'There are currently no record exist', 'result': False}
    table_keys = get_table_keys(table, not_contain_keys=not_contain_keys)
    if table == DeviceTopology:
        all_result = [[topology for topology in eval(obj.topology)] for obj in results]
    else:
        all_result = [header] + [[getattr(obj, key) for key in table_keys] for obj in results]
    data = excel.make_response_from_array(all_result, "xls", file_name=filename)
    return {'message': 'success', 'result': True, 'data': data}


def handle_change_password(table, datadict, identity):
    username = datadict.get('username')
    try:
        if identity == 'admin':
            new_pwd = encrypt_password(datadict.get('password'))
            if not session.query(table).filter_by(username=username).first():
                return {'message': 'The current user does not exist', 'result': False}
            session.query(table).filter_by(username=username).update({table.password: new_pwd})
        if identity == 'user':
            pwd, new_pwd = encrypt_password(datadict.get('password')), encrypt_password(datadict.get('new_password'))
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


def handle_login(table, datadict):
    username = datadict.get('username')
    password = encrypt_password(datadict.get('password'))
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
