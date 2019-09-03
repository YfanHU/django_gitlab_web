from django.shortcuts import render, redirect
from django.http import HttpResponse, FileResponse
from gitlab_web.logger import Logger
import json
from gitlab_web.utils import myutils, specific_utils, send_email
from datetime import datetime, timedelta
from gitlab_web.utils.rsa_utils import *
from random import randint


# Create your views here.
def test(request):
    # privatekey = myutils.sql_query_one('''
    # select privatekey from account_sharing_admin_rsa where uid = 1
    # ''')['privatekey']
    # # pubkey,privkey = [result['publickey'],result['privatekey']]
    # # test_msg = rsa_encrypt(pubkey,'asdf')
    # with open('1.txt','wb') as f:
    #     f.write(bytes(privatekey,encoding='utf-8'))
    # f= open('1.txt','rb')
    # # msg = f.read()
    # response = FileResponse(f)
    # response['Content-Type']='application/octet-stream'
    # response['Content-Disposition']='attachment;filename="Apoca.code"'
    # return response
    # test_msg = rsa_decrypt(privkey,msg)
    # return render(request,'index.html',context={'test_msg':test_msg})
    # return redirect('hyf2019.com')
    return redirect('hyf2019.com')


def download(request):
    download_url = request.GET.get('file_path')
    print('收到download请求:', download_url)
    if download_url:
        middle_dir = download_url.split('/')[1]
        f = open(download_url, 'rb')
        # msg = f.read()
        response = FileResponse(f)
        response['Content-Type'] = 'application/octet-stream'
        if middle_dir == 'code_files':
            response['Content-Disposition'] = 'attachment;filename="code.code"'
        elif middle_dir == 'client':
            if download_url[-4:] == '.exe':
                response['Content-Disposition'] = 'attachment;filename="decryption.exe"'
            else:
                response['Content-Disposition'] = 'attachment;filename="private.code"'
        else:
            response['Content-Disposition'] = 'attachment;filename="我也不知道你想下载啥"'
        return response
    else:
        return HttpResponse('该链接已失效，请重新申请')


def index(request):
    return render(request, 'index.html')


# 进入account_sharing界面
def account_sharing(request):
    if request.COOKIES.get('admin_username', None):
        print('# 进入account_sharing界面,已登录')
        return render(request, 'account_sharing/index.html', context={
            'verify_status': False,
            'verify_result': '',
        })
    else:
        print('# 进入account_sharing界面,未登录')
        response = render(request, 'account_sharing/admin_login.html')
        response.set_cookie('history', '/account_sharing', 600)
        return response


# 进入管理员登陆界面
def account_admin(request):
    if request.COOKIES.get('admin_username', None):
        return redirect('/account_sharing/admin/login')
    else:
        return render(request, 'account_sharing/admin_login.html')


# 管理员登陆
def account_admin_login(request):
    # 若已登录
    if request.COOKIES.get('admin_username', None):
        print('进入管理员登陆界面,已登录')
        uid = myutils.sql_query_one('''select uid from account_sharing_admin_info where admin_username = "{}"'''
                                    .format(request.COOKIES.get('admin_username')))['uid']
        account_list = myutils.sql_query_all('''select * from account_sharing_account_info''')
        apply_history_list = myutils.sql_query_all(
            ''' select * from account_sharing_account_history where uid = {} order by end_time desc limit 10'''
                .format(uid))
        print(apply_history_list)
        time_now = myutils.get_now()
        apply_history_list.sort(key=lambda x: x['end_time'], reverse=True)
        for i in apply_history_list:
            if i['end_time'] < time_now:
                i['can_cancel'] = '0'
            else:
                i['can_cancel'] = '1'
        admin_apply_info = myutils.sql_query_all('''
        select * from account_sharing_admin_apply_info where admin_username="{}" 
        '''.format(request.COOKIES.get('admin_username')))
        return render(request, 'account_sharing/admin.html',
                      context={'account_list': account_list, 'apply_history_list': apply_history_list,
                               'admin_apply_info': admin_apply_info})
    # 新的登陆
    if request.method == 'POST':
        admin_name = request.POST['admin_name']
        admin_password = request.POST['admin_password']
        res = myutils.sql_query_one(
            '''select * from account_sharing_admin_info where admin_username = "{}"'''.format(admin_name))
        print('here : ', res)
        if res:
            if res['admin_password'] == admin_password:
                Logger().add_log('{} : {} 登陆成功'.format(myutils.get_now(), admin_name))
                if request.COOKIES.get('history', None):
                    print('进入管理员登陆界面,已登录，返回历史网页')
                    response = redirect(request.COOKIES.get('history'))
                    response.delete_cookie('history')
                else:
                    print('进入管理员登陆界面,已登录，返回账号网页')
                    # account_list = myutils.sql_query_all('''select * from account_sharing_account_info''')
                    # response = render(request,'account_sharing/admin.html',context={'account_list':account_list})
                    response = redirect('/account_sharing/admin/login')
                response.set_cookie('admin_username', admin_name, 600)
                return response
        adimn_login_info = '用户密码不正确请重新输入'
        return render(request, 'account_sharing/admin_login.html', context={'adimn_login_info': adimn_login_info})
    else:
        return redirect('/account_sharing/admin')


def account_admin_logout(request):
    response = redirect('/account_sharing/admin')
    response.delete_cookie('admin_username')
    response.delete_cookie('verify_status')
    return response


def account_admin_change_password(request):
    admin_username = request.COOKIES.get('admin_username', '')
    if admin_username:
        if request.method == 'GET':
            # admin_info = myutils.sql_query_one('''
            # select * from account_sharing_admin_info where admin_username="{}"'''.format(admin_username))
            return render(request, 'account_sharing/admin_change_password.html',
                          context={'admin_username': admin_username})
        if request.method == 'POST':
            admin_info = myutils.sql_query_one('''
            select * from account_sharing_admin_info where admin_username="{}"'''.format(admin_username))
            admin_password = request.POST['password_old']
            if admin_password == admin_info['admin_password']:
                admin_new_password = request.POST['password_new']
                myutils.sql_modify('''
                update account_sharing_admin_info set admin_password="{}" where admin_username="{}"
                '''.format(admin_new_password, admin_username))
                response = render(request, 'account_sharing/admin_login.html',
                                  context={'adimn_login_info': '密码修改成功，请重新登陆'})
                response.delete_cookie('admin_username')
                return response
            else:
                return render(request, 'account_sharing/admin_change_password.html',
                              context={'admin_username': admin_username, 'warning_text': '原密码输入错误！'})

    return redirect('account_sharing/admin_login')


def account_admin_update(request):
    if request.method == 'GET':
        aid = request.GET.get('aid')
        if aid == '-999':
            return render(request, 'account_sharing/admin_add.html')
        else:
            account_info = myutils.sql_query_one(
                ''' select * from account_sharing_account_info where aid = {} '''.format(aid))
            print(aid)
            return render(request, 'account_sharing/admin_update.html', context=account_info)


def account_admin_add(request):
    context = dict()
    if not request.COOKIES.get('admin_username', ''):
        return redirect('/account_sharing/admin/login')
    if request.method == 'POST':
        print(request.POST)
        account_name = request.POST['account_name']
        account_password = request.POST['account_password']
        account_expire_time = request.POST['account_expire_time']
        account_type = request.POST['account_type']
        if account_name and account_password:
            if myutils.sql_query_one(''' select * from account_sharing_account_info where account_name="{}"'''.format(
                    account_name)) is None:
                if myutils.get_now()[:10] < account_expire_time:
                    apply_sql = '''insert into account_sharing_account_info (account_name, account_password, account_start_time, account_expire_time, account_type) values (""{}"",""{}"",""{}"",""{}"",""{}"")'''.format(
                        account_name, account_password, myutils.get_now()[:10], account_expire_time, account_type)
                    apply_content = '新增游戏共享账号 {}；账号类型 {}'.format(account_name, account_type)
                    myutils.sql_modify(
                        ''' insert into account_sharing_admin_apply_info (apply_time, admin_username, apply_content, apply_sql, apply_status) values ("{}","{}","{}","{}","{}")'''.format(
                            myutils.get_now(), request.COOKIES.get('admin_username'), apply_content, apply_sql,
                            'waiting'))
                    return redirect('/account_sharing/admin/login')
                else:
                    context['warning_text'] = '过期时间应大于当前时间'
            else:
                context['warning_text'] = '该账号已存在，如需更变，请删除已有账号后新增'
        else:
            context['warning_text'] = '请输入账号密码'
        return render(request, 'account_sharing/admin_add.html', context=context)


def account_admin_delete(request):
    admin_username = request.COOKIES.get('admin_username', '')
    if admin_username:
        aid = request.GET['aid']
        apply_sql = 'delete from account_sharing_account_info where aid = {}'.format(aid)
        account_name = myutils.sql_query_one('''select account_name from account_sharing_account_info where aid={}'''
                                             .format(aid))['account_name']
        apply_content = '删除游戏共享账号 {} '.format(account_name)
        if myutils.sql_query_one('''
        select * from account_sharing_admin_apply_info where apply_sql="{}" and apply_status="waiting"
        '''.format(apply_sql)):
            return HttpResponse('已存在该请求')
        else:
            myutils.sql_modify('''insert into account_sharing_admin_apply_info 
            (apply_time, admin_username, apply_content, apply_sql, apply_status) values ("{}","{}","{}","{}","{}")'''
                               .format(myutils.get_now(), request.COOKIES.get('admin_username'), apply_content,
                                       apply_sql, 'waiting'))
            return HttpResponse('success')
    else:
        return HttpResponse('用户信息超时')


def account_history_delete(request):
    myutils.sql_modify('delete from account_sharing_account_history where id = {}'.format(request.GET['id']))
    return HttpResponse('success')


def account_admin_register(request):
    if request.method == 'GET':
        return render(request, 'account_sharing/admin_register.html')

    else:
        admin_username = request.POST['admin_username']
        admin_password = request.POST['admin_password']
        email = request.POST['email']
        invitation_code = request.POST['invitation_code']
        if specific_utils.check_admin_username_in_db(admin_username):
            return render(request, 'account_sharing/admin_register.html', context={'warning_text': '用户已存在'})
        if specific_utils.check_admin_username_in_awaiting_db(admin_username):
            return render(request, 'account_sharing/admin_register.html', context={'warning_text': '用户正在审批中'})
        if not specific_utils.check_invitation_code(invitation_code):
            return render(request, 'account_sharing/admin_register.html', context={'warning_text': '邀请码不正确'})

        myutils.sql_modify('''insert into account_sharing_admin_register_info 
        (admin_username, admin_password, status, email, register_time) 
        VALUES ("{}","{}","{}","{}","{}")'''.format(admin_username, admin_password, 'waiting', email,
                                                    myutils.get_now()[:10]))

        return HttpResponse('注册请求成功，请等待,我们将以邮件形式发送注册状态给您')


# 进入account_sharing界面，输入验证码
def account_sharing_verify(request):
    if request.COOKIES.get('admin_username', None) is None:
        print('进入account_sharing界面,还未登陆')
        response = redirect('/account_sharing/admin/login')
        response.set_cookie('history', '/account_sharing', 600)
        return response
    context = dict()
    if request.COOKIES.get('verify_status', ''):
        context['verify_status'] = 'success'
        context['log_content'] = myutils.show_account_status_for_user()
    if request.method == 'POST':
        context['verify_status'] = 'error'
        context['verify_result'] = ''
        input_code = request.POST['recognition_code']
        print(input_code)
        db_code = myutils.sql_query_one('''
        select admin_verification_code from account_sharing_admin_info where admin_username ="{}"'''
                                        .format(request.COOKIES.get('admin_username')))['admin_verification_code']
        if input_code == db_code:
            need_set_cookie = True
            context['verify_status'] = 'success'
            context['log_content'] = myutils.show_account_status_for_user()
        else:
            context['verify_result'] = '识别码输入错误，请重新来过！'
    try:
        if need_set_cookie:
            response = render(request, 'account_sharing/index.html', context=context)
            response.set_cookie('verify_status', True, 600)
            return response
    except:
        pass

    return render(request, 'account_sharing/index.html', context=context)


# /account_sharing/add_log/2019-08-23%2015:55:08/4h
# 申请
def add_log(request, apply_time, period, type):
    if request.COOKIES.get('admin_username', None) is None:
        return redirect('/account_sharing/admin')
    # apply_time='2019-08-21 15:20:48'
    # period='1h'
    context = dict()
    have_available, aid = myutils.have_available_account(apply_time, type=type)
    datetime_now = datetime.now()
    datetime_period = timedelta(hours=int(period[:-1]))
    datetime_end = datetime_now + datetime_period

    if have_available:
        uid = myutils.get_uid_by_admin_username(request.COOKIES.get('admin_username'))
        max_account_nb = \
            myutils.sql_query_one(
                ''' select max_account_nb from account_sharing_admin_info where uid={} '''.format(uid))[
                'max_account_nb']
        cur = myutils.current_inused_account_number_for_user(uid)
        print('cur:{},max_account_nb:{}'.format(cur,max_account_nb))
        if cur >= max_account_nb :
            log_text = ' '.join(['Apply time :', apply_time, 'Apply period :', period, 'status : fail'])
            context['apply_use_result_info'] = ' '.join([apply_time, ': 申请失败.','已达到当前使用账号上限'])
            context['download_code_url'] = ''
        else :
            account_name = \
                myutils.sql_query_one(
                    ''' select account_name from account_sharing_account_info where aid={} '''.format(aid))[
                    'account_name']
            myutils.sql_modify(
                '''insert into account_sharing_account_history (aid,account_name,apply_time,apply_duration,end_time,uid) values ({},"{}","{}","{}","{}",{})'''
                    .format(aid, account_name, myutils.get_now(), period, datetime_end.__str__()[:19], uid, ))
            log_text = ' '.join(
                ['Apply time :', apply_time, 'Apply period :', period, 'status : success', 'account_name :', account_name])
            context['apply_use_result_info'] = ' '.join(
                [apply_time, ': 已成功申请', period, '时长', '分配账号为：{}'.format(account_name)])
            # 生成密码文件以及返回文件路径
            file_path = myutils.generate_code_file(uid, account_name)
            context['download_code_url'] = '''
            <a href="/download/?file_path={}">点击此处下载密码</a>
            '''.format(file_path)

    else:
        log_text = ' '.join(['Apply time :', apply_time, 'Apply period :', period, 'status : fail'])
        context['apply_use_result_info'] = ' '.join([apply_time, ': 申请失败'])
        context['download_code_url'] = ''
    print(log_text)
    Logger().add_log(log_text)

    # context['verify_status'] = 'success'
    # context['verify_result'] = ''
    context['log_content'] = myutils.show_account_status_for_user()
    return HttpResponse(json.dumps(context), content_type="application/json")

    # return HttpResponse(Logger().show_log())


def super_admin(request):
    context = dict()
    if request.method == "GET":
        if request.COOKIES.get('super_admin_name', ''):
            pass
        else:
            return render(request, 'super/super_login.html')
    else:
        super_admin_password = request.POST['password']
        if super_admin_password != 'super':
            return render(request, 'super/super_login.html', context={'login_msg': '密码输入错误'})

    context['admin_list'] = myutils.sql_query_all('''select * from account_sharing_admin_info''')
    context['apply_list'] = myutils.sql_query_all(
        '''select * from account_sharing_admin_apply_info where apply_status="waiting"''')
    context['register_list'] = myutils.sql_query_all(
        ''' select * from account_sharing_admin_register_info where status ="waiting"''')
    response = render(request, 'super/super.html', context=context)
    response.set_cookie('super_admin_name', 'super', 600)
    return response


def super_delete_admin(request):
    if request.COOKIES.get('super_admin_name', ''):
        try:
            uid = request.GET['uid']
            myutils.sql_modify('''delete from account_sharing_admin_info where uid={}'''.format(uid))
            return HttpResponse('success')
        except:
            pass
    return HttpResponse('fail')


def super_approve_apply(request):
    if request.COOKIES.get('super_admin_name', ''):
        try:
            apply_id = request.GET['apply_id']
            myutils.sql_modify('''
            update account_sharing_admin_apply_info set apply_status="approved" where apply_id={}
            '''.format(apply_id))
            apply_sql = \
            myutils.sql_query_one('''select apply_sql from account_sharing_admin_apply_info where apply_id={}'''
                                  .format(apply_id))['apply_sql']
            myutils.sql_modify(apply_sql)
            return HttpResponse('success')
        except:
            pass
    return HttpResponse('fail')


def super_refuse_apply(request):
    if request.COOKIES.get('super_admin_name', ''):
        try:
            apply_id = request.GET['apply_id']
            myutils.sql_modify('''
            update account_sharing_admin_apply_info set apply_status="refused" where apply_id={}
            '''.format(apply_id))
            return HttpResponse('success')
        except:
            pass
    return HttpResponse('fail')


def super_approve_register(request):
    if request.COOKIES.get('super_admin_name', ''):
        try:
            register_id = request.GET['register_id']
            admin_info = myutils.sql_query_one(
                '''select * from account_sharing_admin_register_info where register_id={}'''
                .format(register_id))
            print(admin_info)
            admin_username = admin_info['admin_username']
            admin_password = admin_info['admin_password']
            admin_register_time = admin_info['register_time']
            admin_email = admin_info['email']
            admin_verification_code = ''.join([str(randint(0, 10)) for _ in range(4)])
            admin_info['admin_verification_code'] = admin_verification_code
            # TODO ：发送邮件
            if not send_email.send_email(admin_email, admin_info):
                return HttpResponse('fail')
            myutils.sql_modify('''
            update account_sharing_admin_register_info set status="confirmed" where register_id={}
            '''.format(register_id))
            myutils.sql_modify('''insert into account_sharing_admin_info 
            (admin_username, admin_password, admin_verification_code, admin_register_time, admin_email) 
            VALUES ("{}","{}","{}","{}","{}")'''.format(admin_username, admin_password, admin_verification_code,
                                                        admin_register_time, admin_email))

            uid = myutils.get_uid_by_admin_username(admin_username)
            publickey, privatekey = rsa_new_keys()
            with open('files/client/{}.code'.format(admin_username), 'wb') as f:
                f.write(bytes(privatekey, encoding='utf-8'))
            myutils.sql_modify(''' insert into account_sharing_admin_rsa 
            (uid, publickey, privatekey) VALUES ({},"{}","{}")'''.format(uid, publickey, privatekey))
            return HttpResponse('success')
        except:
            pass
    return HttpResponse('fail')


def super_refuse_register(request):
    if request.COOKIES.get('super_admin_name', ''):
        try:
            register_id = request.GET['register_id']
            admin_info = myutils.sql_query_one(
                '''select * from account_sharing_admin_register_info where register_id={}'''
                    .format(register_id))
            admin_username = admin_info['admin_username']
            admin_email = admin_info['email']
            # TODO : 发送邮件
            if not send_email.send_email(admin_email):
                return HttpResponse('fail')
            myutils.sql_modify('''
            update account_sharing_admin_register_info set status="rejected" where register_id={}
            '''.format(register_id))
            return HttpResponse('success')
        except:
            pass
    return HttpResponse('fail')


def admin_delete_apply(request):
    if request.COOKIES.get('admin_username', ''):
        try:
            apply_id = request.GET['apply_id']
            myutils.sql_modify('''
            delete from account_sharing_admin_apply_info where apply_id={}
            '''.format(apply_id))
            return HttpResponse('success')
        except:
            pass
    return HttpResponse('fail')
