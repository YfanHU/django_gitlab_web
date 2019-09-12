"""django_gitlab_web URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,re_path
from gitlab_web.views import functional_views,views,views_qqmusic_download

urlpatterns = [
    # path('admin/', admin.site.urls),
    path('download/',views.download),
    path('hyf2019.com',views.index),
    path('account_sharing',views.account_sharing_verify),

    path('super', views.super_admin),
    path('super/delete_admin/',views.super_delete_admin),
    path('super/approve_apply/',views.super_approve_apply),
    path('super/refuse_apply/',views.super_refuse_apply),
    path('super/approve_register/', views.super_approve_register),
    path('super/refuse_register/', views.super_refuse_register),

    re_path(r'^test/?$', views.test),
    path('account_sharing/verify_code',views.account_sharing_verify),
    path('account_sharing/admin',views.account_admin),
    path('account_sharing/admin/login',views.account_admin_login),
    path('account_sharing/admin/logout',views.account_admin_logout),
    path('account_sharing/admin/change_password',views.account_admin_change_password),
    path('account_sharing/admin/register',views.account_admin_register),
    path('account_sharing/admin/update_account/',views.account_admin_update),
    path('account_sharing/admin/add_account',views.account_admin_add),
    path('account_sharing/admin/delete_account/',views.account_admin_delete),
    path('account_sharing/admin/delete_history/',views.account_history_delete),
    path('account_sharing/admin/delete_apply/',views.admin_delete_apply),
    path('account_sharing/verify_admin_username/',functional_views.account_sharing_verify_admin_username),
    path('account_sharing/verify_invitation_code/', functional_views.account_sharing_verify_invitation_code),
    # /account_sharing/add_log/2019-08-23%2015:55:08/4h
    re_path(r'^account_sharing/add_log/(.+)/(\w+)/(\w+)$',views.add_log),

    path('music_download',views_qqmusic_download.index),
    path('music_download/qqmusic_download',views_qqmusic_download.download_music),
]
