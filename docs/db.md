# 数据库设计
## 数据格式
时间 : ‘yyyy-mm-dd’‘yyyy-mm-dd HH:MM:SS’

    '2019-08-21 15:20:48'
## 表清单

- account_sharing_admin_info
    - uid : user_id
    - admin_username (unique)
    - admin_password
    - admin_verification_code
    - admin_register_time 

- account_sharing_register_info
    - register_id
    - admin_username
    - admin_password
    - status : 
      - 'waiting'
      - 'confirmed'
      - 'rejected'
    - email
    - register_time

- account_sharing_admin_rsa
    - uid :
    - publickey
    - privatekey
    
- account_sharing_account_info
    - aid : account_id
    - account_name (unique)
    - account_password
    - account_type
    - account_start_time
    - account_expire_time

- account_sharing_account_history
    - id :
    - aid :
    - uid :
    - account_name :
    - apply_time :
    - apply_duration :
    - other_info :

- account_sharing_admin_apply_info
    - apply_id : 
    - apply_time :
    - admin_username :
    - apply_content :
    - apply_sql :
    - apply_status : 
        - 'waiting' : 等待审批,
        - 'approved' : 已审批,
        - 'finished': 完成
        - 'refused':
    
    
## cookies
- verify_status : 是否输入过用户验证码
- admin_username : 登陆的用户名
- history : 登陆后的跳转页面链接
- super_admin : 超级管理员是否登陆