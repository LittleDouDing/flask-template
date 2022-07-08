from apps.models.models import DeviceTopology, MultipleAccount, User, Admin
from apps.utils.util_tool import get_table_keys, get_database_err
from apps.utils.route_tool import check_topology
from apps.utils.route_tool import get_topology, get_device_ip, get_network_topology
from apps.models import db
import flask_excel as excel
import datetime
import xlrd

session = db.session
not_contain_keys = ['device_id', 'port_id', 'topology_id', 'network_id', 'multiple_id']


def handle_search_info(table, datadict):
    page = int(datadict.get('page')) if datadict.get('page') else 1
    datadict = {key: datadict.get(key) for key in datadict if datadict.get(key)}
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
            setattr(obj, k, datadict.get(k))
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
            obj = session.query(table).filter(getattr(table, key) == datadict.get(key)).first()
            session.delete(obj)
            session.commit()
            return {'message': 'The record has been successfully deleted', 'result': True}
        except Exception as e:
            session.rollback()
            return {'message': get_database_err(e), 'result': False}
    return {'message': 'The current record does not exist', 'result': False}


def handle_add_info(table, datadict, keys):
    conditions = (getattr(table, key) == datadict.get(key) for key in keys)
    if not session.query(table).filter(*conditions).first():
        try:
            result = check_topology(datadict.get('topology')) if 'topology' in keys else {'result': True}
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


def handle_upload_file(uploaded_file, table, header=None, require_cols=None):
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
        for i in range(start_index, sheet.nrows):
            obj = table()
            if table != DeviceTopology:
                for j in range(sheet.ncols):
                    cell_value = sheet.row_values(i)[j]
                    if j in require_cols and not cell_value:
                        table_key = ' '.join(table_keys[j].split('_'))
                        return {'message': 'The ' + table_key + ' cant not be empty', 'result': False}
                    if 'time' in table_keys[j]:
                        data = datetime.datetime(1900, 1, 1) + datetime.timedelta(cell_value - 2)
                    else:
                        data = str(int(cell_value)) if isinstance(cell_value, float) else str(cell_value).strip()
                    setattr(obj, table_keys[j], data)
            else:
                for j in range(sheet.ncols):
                    cell_value = sheet.row_values(i)[j]
                    if ':' not in sheet.row_values(i)[j]:
                        return {'message': 'The format of topology ' + cell_value + ' is illegal', 'result': False}
                    result = check_topology([str(cell_value).strip()])
                    if not result.get('result'):
                        return {'message': result.get('message'), 'result': False}
                topology = str([sheet.row_values(i)[j].replace("'", '"').strip() for j in range(sheet.ncols)])
                setattr(obj, 'topology', topology)
            obj_list.append(obj)
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


def handle_search_topology(datadict):
    datadict = {'topology': datadict.get('device_name')} if datadict.get('device_name') else {}
    result = handle_search_info(DeviceTopology, datadict)
    data = result.get('data')
    if data:
        results = data.get('results')
        for idx, res in enumerate(results):
            topology_list = eval(res.get('topology'))
            result['data']['results'][idx]['topology_list'] = topology_list
            result['data']['results'][idx]['topology'] = get_topology(eval(res['topology']))
            result['data']['results'][idx]['device_ip'] = get_device_ip(topology_list)
    return result


def handle_search_multiple_account(table, datadict):
    result = handle_search_info(table, datadict)
    data = result.get('data')
    if data:
        results = data.get('results')
        for idx, res in enumerate(results):
            result['data']['results'][idx]['main_topology'] = eval(res.get('main_topology'))
            result['data']['results'][idx]['main_access'] = eval(res.get('main_access'))
            result['data']['results'][idx]['main_devices'] = eval(res.get('main_devices'))
            main_network_topology = get_network_topology(get_topology(res['main_topology']), res['main_access'])
            result['data']['results'][idx]['main_network_topology'] = main_network_topology
            result['data']['results'][idx]['open_time'] = datetime.datetime.strftime(res.get('open_time'), '%Y-%m-%d')
            if res.get('backup_topology'):
                result['data']['results'][idx]['backup_topology'] = eval(res.get('backup_topology'))
            if res.get('backup_access'):
                result['data']['results'][idx]['backup_access'] = eval(res.get('backup_access'))
            if res.get('backup_devices'):
                result['data']['results'][idx]['backup_devices'] = eval(res.get('backup_devices'))
            if res.get('backup_topology') and res.get('backup_access'):
                backup_topology = get_topology(res['backup_topology'])
                backup_network_topology = get_network_topology(backup_topology, res['backup_access'])
                result['data']['results'][idx]['backup_network_topology'] = backup_network_topology
    return result


def handle_search_network_account(table, datadict):
    result = handle_search_info(table, datadict)
    data = result.get('data')
    if data:
        results = data.get('results')
        for idx, res in enumerate(results):
            result['data']['results'][idx]['ip_address'] = eval(res.get('ip_address'))
            result['data']['results'][idx]['mask_router_dns'] = eval(res.get('mask_router_dns'))
            result['data']['results'][idx]['topology'] = eval(res.get('topology'))
            result['data']['results'][idx]['access_information'] = eval(res.get('access_information'))
            network_topology = get_network_topology(get_topology(res['topology']), res['access_information'])
            result['data']['results'][idx]['network_topology'] = network_topology
            result['data']['results'][idx]['relate_device'] = eval(res.get('relate_device'))
            finish_time = datetime.datetime.strftime(res.get('finnish_time'), '%Y-%m-%d')
            result['data']['results'][idx]['finnish_time'] = finish_time
    return result


def handle_get_topology(datadict):
    device_name = datadict.get('device_name')
    device_type = datadict.get('device_type')
    if device_type == 'Switch':
        port = datadict.get('port')
        if not port:
            return {'message': 'The port cannot be empty', 'result': False}
        device_port = device_name + ':' + port
        results = session.query(DeviceTopology).filter(DeviceTopology.topology.like('%' + device_port + '%'))
        for res in results:
            topology = eval(res.topology)
            if topology[-1] == device_port:
                data = {'topology': topology, 'relate_device': get_device_ip(topology)}
                return {'message': 'success', 'data': data, 'result': True}
    else:
        condition = MultipleAccount.multiple_name.like('%' + device_name + '%')
        result = session.query(MultipleAccount).filter(condition).first()
        main_topology, main_access = eval(result.main_topology), eval(result.main_access)
        main_devices = eval(result.main_devices)
        data = {'topology': main_topology, 'access_information': main_access, 'relate_device': main_devices}
        return {'message': 'success', 'data': data, 'result': True}
    return {'message': 'The topology does not exist', 'result': False}
