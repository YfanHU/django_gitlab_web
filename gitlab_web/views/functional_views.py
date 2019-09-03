from django.http import HttpResponse,FileResponse
import json
from gitlab_web.utils import specific_utils
# HttpResponse(json.dumps(context), content_type="application/json")

def account_sharing_verify_admin_username(request):
    context = dict()
    if specific_utils.check_admin_username_in_db(request.GET['admin_username']):
        context['status'] = 'fail'
        context['msg'] = '账号已存在'
    else :
        context['status']='success'
    return HttpResponse(json.dumps(context),content_type='application/json')

def account_sharing_verify_invitation_code(request):
    context = dict()
    if specific_utils.check_admin_username_in_awaiting_db(request.GET['admin_username']):
        context['status'] = 'fail'
        context['msg'] = '账号正在审批中'
    else :
        context['status']='success'
    return HttpResponse(json.dumps(context),content_type='application/json')