import sqlite3
from datetime import datetime
from gitlab_web.utils.rsa_utils import *


def get_now():
    # 获取当前时间
    # 2019-08-21 15:20:48
    return datetime.now().__str__()[:19]


def have_available_account(apply_time, type='NORMAL'):
    # apply_time='2019-08-21 15:20:48'
    '''

    :param apply_time:
    :param type:
    :return: True aid; False None
    '''
    aid_list = sql_query_all(
        '''select aid from account_sharing_account_info where account_type = "{}"'''
            .format(type))
    for aid in aid_list:
        end_time = sql_query_one(
            '''select end_time from account_sharing_account_history where aid = {} order by end_time desc '''
                .format(aid['aid']))
        if not end_time or end_time['end_time'] <= get_now():
            return True, aid['aid']
    return False, None


def account_status_for_user():
    aid_list = sql_query_all(
        '''select aid,account_name from account_sharing_account_info'''
    )
    res = []
    for aid in aid_list:
        temp_dic = dict()
        temp_dic['account_name'] = aid['account_name']
        end_time = sql_query_one(
            '''select end_time from account_sharing_account_history where aid = {} order by end_time desc '''
                .format(aid['aid']))
        if end_time:
            if end_time['end_time'] <= get_now():
                temp_dic['availability'] = '可用'
            else:
                temp_dic['availability'] = '不可用（%s）' % (end_time['end_time'])
        else:
            temp_dic['availability'] = '可用'
        res.append(temp_dic)
    return res


def current_inused_account_number_for_user(uid):
    apply_history_list = sql_query_all(
        ''' select * from account_sharing_account_history where uid = {} order by end_time desc limit 10'''
            .format(uid))
    time_now = get_now()
    apply_history_list.sort(key=lambda x: x['end_time'], reverse=True)
    count = 0
    for i in apply_history_list:
        if i['end_time'] < time_now:
            break
        else:
            count+=1
    return count


def show_account_status_for_user():
    header = ['<thead><tr>', '</tr></thead>']
    contenter = ['<td>', '</td>']
    col_names = ['account', 'availability']
    head_str = ''.join([col_name.join(['<th>', '</th>']) for col_name in col_names]).join(header)
    content_str = ''.join(
        [(dic['account_name'].join(contenter) + dic['availability'].join(contenter)).join(['<tr>', '</tr>']) for dic in
         account_status_for_user()])
    return (head_str + content_str).join(['<table>', '</table>'])


def sql_modify(query_str):
    print(query_str)
    conn = sqlite3.connect('db.sqlite3')
    conn.row_factory = dict_factory
    print("Opened database successfully")
    c = conn.cursor()
    c.execute(query_str)
    print("Query successfully")
    conn.commit()
    res = conn.total_changes
    conn.close()
    return res


def sql_query_all(query_str):
    conn = sqlite3.connect('db.sqlite3')
    conn.row_factory = dict_factory
    print("Opened database successfully")
    c = conn.cursor()
    c.execute(query_str)
    print("Query successfully")
    result = c.fetchall()
    conn.close()
    return result


def sql_query_one(query_str):
    conn = sqlite3.connect('db.sqlite3')
    conn.row_factory = dict_factory
    print("Opened database successfully")
    c = conn.cursor()
    c.execute(query_str)
    print("Query successfully")
    result = c.fetchone()
    conn.close()
    return result


def sql_test():
    conn = sqlite3.connect('db.sqlite3')
    print("Opened database successfully")
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS TEST
           (ID INT PRIMARY KEY     NOT NULL,
           NAME           TEXT    NOT NULL,
           AGE            INT     NOT NULL,
           ADDRESS        CHAR(50),
           SALARY         REAL);''')
    print("Table created successfully")
    conn.commit()
    conn.close()


def get_uid_by_admin_username(admin_username):
    print('get_uid_by_admin_username', admin_username)
    return \
    sql_query_one('''select uid from account_sharing_admin_info where admin_username="{}"'''.format(admin_username))[
        'uid']


def generate_code_file(uid, account_name):
    public_key = sql_query_one('''
    select publickey from account_sharing_admin_rsa where uid = {}
    '''.format(uid))['publickey']
    account_password = sql_query_one('''
    select account_password from account_sharing_account_info where account_name = "{}"
    '''.format(account_name))['account_password']
    time_now = get_now().split(' ')

    file_name = str(uid) + time_now[0] + ''.join(time_now[1].split(':')) + '.code'
    file_path = 'files/code_files/' + file_name
    with open(file_path, 'wb') as f:
        f.write(rsa_encrypt(public_key, account_password))
    return file_path


def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d
