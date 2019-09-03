from gitlab_web.utils import myutils

def check_admin_username_in_db(admin_username):
    '''

    :param admin_username:
    :return: True : if exist
    '''
    return True if myutils.sql_query_one('''
    select * from account_sharing_admin_info where admin_username="{}"
    '''.format(admin_username)) else False

def check_admin_username_in_awaiting_db(admin_username):
    return True if myutils.sql_query_one('''
    select * from account_sharing_admin_register_info where admin_username="{}"
    '''.format(admin_username)) else False

def check_invitation_code(invitation_code):
    return True if invitation_code=='hyf2019' else False