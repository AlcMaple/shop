# Flask:创建web应用
# request：获取客户端请求的信息
# jsonify：将python字典转换为Json响应
from flask import Flask, request, jsonify

import pymysql.cursors
import random

#
# 开发者平台：https://quanmwl.yuque.com/lx4ve0/vcsmy6/gwsgnw
# 使用泉鸣开发短信平台：https://index.dev.quanmwl.com/
#

from quanmsms import sdk  # pip install quanmsms

from flask_jwt_extended import create_access_token,JWTManager

import time
import multiprocessing

# 生成足够安全的随机数
import secrets

# os:使用操作系统相关功能
import os

# 创建Flask应用实例
app = Flask(__name__)

connect=pymysql.Connect(
    host='localhost',
    port=7777,
    user='root',
    passwd='loveat2024a+.',
    db='taobao',
    charset='utf8'
)

cursor=connect.cursor()

cursor.execute("Select version()")

version=cursor.fetchone()

print("MySQL数据库版本是：%s"%version)

cursor.close()

# 定义全局变量验证码
verification_code = 0

# 定义全局变量验证手机号
verification_phone = 0

# 步骤：
# 生成安全密钥
# 配置密钥在环境变量中
# 更改生成安全密钥为从环境变量中获取安全密钥

# 配置 JWT
# JWT_SECRET_KEY：编码和解码JWTs的秘密密钥
# 使用 secrets 模块生成一个安全的随机密钥
app.config['JWT_SECRET_KEY'] = secrets.token_urlsafe(32)
# print(app.config['JWT_SECRET_KEY'])

# cmd操作
# 输出密钥后将其配置到环境变量中，使用：setx JWT_SECRET_KEY "your_secret_key"
# 重启cmd后，再验证：echo %JWT_SECRET_KEY%

# 从环境变量中获取安全密钥
app.config['JWT_SECRET_KEY'] = os.environ.get('JWT_SECRET_KEY', 'default_secret_key')
# print(app.config['JWT_SECRET_KEY'])
jwt = JWTManager(app)

# 定义四位数的随机验证码
def generate_verification_code():
     verification_code = str(random.randint(1000, 9999))
     return verification_code

def expire_verification_code():
    # 验证码的有效期为1分钟
    verification_code_expires_in = 60
    time = 0
    global verification_code

    # 1分钟后验证码过期
    while True:
        time+=1
        time.sleep(1)
        if time == verification_code_expires_in:
            verification_code = 1234567890
            break

@app.route('/sendSms',methods=['POST'])
def sendSms():
    start = time.time()
    data = request.json

    global verification_phone
    verification_phone = data.get('phone')

    print("接收到的手机号:", verification_phone)

    # 调用生成验证码函数
    global verification_code
    verification_code = generate_verification_code()

    # 进程任务，设置验证码的有效期为1分钟
    p1 = multiprocessing.Process(target=expire_verification_code)

    p1.start()

    # 打印验证码
    print("验证码是：", verification_code)
    # 调用短信接口，将验证码发送给用户手机号
    sms = sdk.SDK(
        '844',  # OpenID
        '2ec1400212c511efa4d70242ac110002' # Apikey
    )
    # 【基础用法】
    #                                      手机号  模板id   模板参数
    sendOK, info, apiStatus = sms.send(verification_phone, 0, {'code': verification_code})
    print(sendOK) # 是否成功(布尔值)
    print(apiStatus) # api状态码
    print(info) # 描述信息 
    if apiStatus == 200:
        print('短信发送成功')
        # 等待进程执行结束
        p1.join()
        return jsonify({'message': 'Verification code sent successfully'}), 200
    else:
        # 等待进程执行结束
        p1.join()
        print('短信发送失败')
        return jsonify({'error': 'Verification code sent failed'}), 400
    ## 【高级用法，要求sdk版本>=0.2.0】
    #   #                 手机号   模板id   模板参数
    #res = sms.send_raw('19954761564', 0, {'code': 12344})
    #print('状态码：', res.get_code())
    #parsetype, raw = res.get_mess()
    #print(f'mess: {raw},可以使用{parsetype}格式解析这段消息')
    #print('请求id: ', res.get_request_id())
    #print('接口余额: ', res.get_residue())

    # 返回发送验证码成功的JSON响应
    # return jsonify({'message': 'Verification code sent successfully'}), 200

# 定义路由，只接受post方法的http请求
@app.route('/sign', methods=['POST'])
# 与路由关联的函数，获取到请求后执行的函数
def sign():

    data = request.json
    username = data.get('username')
    password = data.get('password')
    phone = data.get('phone')
    checkPass = data.get('checkPass')

    # 打印调试信息
    # print("接收到的用户名:", username)
    # print("接收到的密码:", password)

    # 定义全局变量，以便于使用
    global verification_code
    global verification_phone

    cursor=connect.cursor()

    # 检查用户名是否已被注册
    cursor.execute("SELECT * FROM register WHERE username = %s", [username])
    if cursor.fetchone():
        # 用户名已存在
        cursor.close()
        # 返回一个错误的信息的JSON响应和状态码
        return jsonify({'error': 'Username already exists'}), 400

    # 检查用户名和密码是否为空
    if not username or not password:
        cursor.close()
        return jsonify({'error': 'Username or password are null'}), 400
    
    # 检查手机号是否与发送验证码的手机号一致
    if phone!= verification_phone:
        cursor.close()
        return jsonify({'error': 'verification_phone number is not correct'}), 400

    # 检查验证码是否正确
    if checkPass!= verification_code:
        cursor.close()
        return jsonify({'error': 'Verification code is not correct'}), 400

    # 插入用户数据到数据库
    cursor.execute("INSERT INTO register(username, password,phone) VALUES (%s, %s,%s)", (username, password,phone))

    # 提交事务
    connect.commit()

    # 关闭游标
    cursor.close()

    # 返回成功信息
    return jsonify({'message': 'User registered successfully'}), 201

@app.route('/login',methods=['POST'])
def login():
    res = request.json

    username = res.get('username')
    password = res.get('password')

    # 创建数据库游标对象
    cur = connect.cursor()

    # 执行查询，查找匹配的用户名
    # 获取查询条件的所有结果集
    cur.execute("SELECT * FROM register WHERE username = %s", [username])
    # 从结果集中取出一行，没有则返回none
    user = cur.fetchone()
    # print(user)

    # 如果找到用户并且密码匹配
    if user and password == user[1]:
        # 创建 token，创建前需要配置JWTManager
        access_token = create_access_token(identity=username)
        # 关闭数据库游标
        cur.close()
        # 通过json对象 返回登录成功的消息及 token
        return jsonify({'message': '登录成功', 'access_token': access_token,'username':username}), 200
    else:
        # 关闭数据库游标
        cur.close()
        # 返回登录失败的错误消息
        return jsonify({'error': '用户名或密码错误'}), 401

# 检查验证码是否正确
@app.route('/checkCode',methods=['POST'])
def checkCode():
    data = request.json
    phone = data.get('phone')
    checkPass = data.get('checkPass')
    # 检查手机号是否与发送验证码的手机号一致
    if phone!= verification_phone:
        cursor.close()
        return jsonify({'error': 'verification_phone number is not correct'}), 400

    # 检查验证码是否正确
    if checkPass!= verification_code:
        cursor.close()
        return jsonify({'error': 'Verification code is not correct'}), 400

# # 验证token的有效性
# # @app.route('/protected',methods=['GET'])
# # def protected():
# #     try:
# #         # 验证JWT
# #         verify_jwt_in_request()
# #         # 获取token中的用户身份信息
# #         current_user = get_jwt_identity()
# #         return jsonify(logged_in_as=current_user), 200
# #     except:
# #         return jsonify(msg="Invalid token"), 401

# 获取用户列表数据
@app.route('/users',methods=['POST'])
def users():

    data = request.json
    # 查询的内容
    query = data.get('query')
    # 总页码数
    pageSize = data.get('pageSize')
    # 当前页码数
    pageNum = data.get('pageNum')

    # 创建数据库游标对象
    cur = connect.cursor()

    # 计算每页显示的记录数
    records_per_page = pageSize

    # 计算OFFSET值
    offset = (pageNum - 1) * records_per_page

    # 执行查询，根据查询内容、当前页码和每页显示的记录数来获取数据
    cur.execute(f"SELECT * FROM user WHERE username LIKE %s LIMIT %s OFFSET %s", 
                ('%' + query + '%', records_per_page, offset))

    # 获取查询结果
    users = cur.fetchall()

    # 关闭数据库游标
    cur.close()

    # 通过json对象 返回用户列表数据
    return jsonify({'users': users}), 200

@app.route('/addUser',methods=['POST'])
def addUser():
    data = request.json

    username = data.get('username')
    phone = data.get('phone')
    email = data.get('email')

    # 创建数据库游标对象
    cur = connect.cursor()

    # 执行插入语句，插入用户数据
    cur.execute("INSERT INTO user(username,phone,email,roles,status) VALUES (%s,%s,%s,%s,%s)", (username,phone,email,"用户","true"))

    # 提交事务
    connect.commit()

    # 关闭数据库游标
    cur.close()

    # 返回成功信息
    return jsonify({'message': 'User added successfully'}), 201

# 获取用户列表总数
@app.route('/usersCount',methods=['POST'])
def usersCount():

    # 获取数据库中用户总数
    cur = connect.cursor()
    cur.execute("SELECT COUNT(*) FROM user")
    count = cur.fetchone()[0]
    # 关闭数据库游标
    cur.close()

    # 通过json对象 返回用户列表总数
    return jsonify({'count': count}), 200

# 更改用户状态
@app.route('/changeStatus',methods=['POST'])
def changeStatus():
    data = request.json

    # 获取用户用户名和状态
    username = data.get('username')
    status = data.get('status')

    if status == "True":
        status = "true"
    else:
        status = "false"

    # 创建数据库游标对象
    cur = connect.cursor()

    # 执行更新语句，更新用户状态
    cur.execute("UPDATE user SET status = %s WHERE username = %s", (status, username))

    # 提交事务
    connect.commit()

    # 关闭数据库游标
    cur.close()

    # 返回成功信息
    return jsonify({'message': 'User status changed successfully'}), 200


# 编辑用户
@app.route('/editUser',methods=['POST'])
def editUser():
    data = request.json

    # 获取用户信息
    phone = data.get('phone')
    email = data.get('email')
    username = data.get('username')

    # 创建数据库游标对象
    cur = connect.cursor()

    # 执行更新语句，更新用户信息
    cur.execute("UPDATE user SET phone = %s, email = %s WHERE username = %s", (phone, email, username))

    # 提交事务
    connect.commit()

    # 关闭数据库游标
    cur.close()

    # 返回成功信息
    return jsonify({'message': 'User edited successfully'}), 200

# 删除用户
@app.route('/deleteUser',methods=['POST'])
def deleteUser():
    data = request.json

    # 获取用户用户名
    username = data.get('username')

    # 创建数据库游标对象
    cur = connect.cursor()

    # 执行删除语句，删除用户
    cur.execute("DELETE FROM user WHERE username = %s", [username])

    # 提交事务
    connect.commit()

    # 关闭数据库游标
    cur.close()

    # 返回成功信息
    return jsonify({'message': 'User deleted successfully'}), 200

# 获取角色列表
@app.route('/roles',methods=['POST'])
def roles():

    # 创建数据库游标对象
    cur = connect.cursor()

    # 执行查询，获取角色列表
    cur.execute("SELECT * FROM rolelist")

    connect.commit()

    # 获取查询结果
    roles = cur.fetchall()

    # 关闭数据库游标
    cur.close()

    # 通过json对象 返回角色列表数据
    return jsonify({'roles': roles}), 200

# 新增角色列表
@app.route('/addRole',methods=['POST'])
def addRole():
    data = request.json

    # 获取角色信息
    roleName = data.get('rolename')
    roleDescription = data.get('roledescription')

    cur = connect.cursor()

    # 执行插入语句，插入角色数据
    cur.execute("INSERT INTO rolelist(RoleName,RoleDescription) VALUES (%s,%s)", (roleName,roleDescription))

    connect.commit()

    # 关闭数据库游标
    cur.close()

    # 返回成功信息
    return jsonify({'message': 'Role added successfully'}), 201

# 修改角色列表信息
@app.route('/editRole',methods=['POST'])
def editRole():
    data = request.json

    # 获取角色信息
    roleName = data.get('rolename')
    roleDescription = data.get('roledescription')
    roleId = data.get('id')

    cur = connect.cursor()

    # 执行更新语句，更新角色信息
    cur.execute("UPDATE rolelist SET RoleName = %s, RoleDescription = %s WHERE id = %s", (roleName,roleDescription,roleId))

    connect.commit()

    # 关闭数据库游标
    cur.close()

    # 返回成功信息
    return jsonify({'message': 'Role edited successfully'}), 200

# 删除角色列表
@app.route('/deleteRole',methods=['POST'])
def deleteRole():
    data = request.json

    roleId = data.get('id')

    cur = connect.cursor()

    # 执行删除语句，删除角色
    cur.execute("DELETE FROM rolelist WHERE id = %s", [roleId])

    connect.commit()

    # 关闭数据库游标
    cur.close()

    # 返回成功信息
    return jsonify({'message': 'Role deleted successfully'}), 200


# 获取用户列表数据
@app.route('/goods',methods=['POST'])
def goods():

    data = request.json
    # 查询的内容
    query = data.get('query')
    # 总页码数
    pageSize = data.get('pageSize')
    # 当前页码数
    pageNum = data.get('pageNum')

    # 创建数据库游标对象
    cur = connect.cursor()

    # 计算每页显示的记录数
    records_per_page = pageSize

    # 计算OFFSET值
    offset = (pageNum - 1) * records_per_page

    # 执行查询，根据查询内容、当前页码和每页显示的记录数来获取数据
    cur.execute(f"SELECT * FROM goodslist WHERE goods_name LIKE %s LIMIT %s OFFSET %s", 
                ('%' + query + '%', records_per_page, offset))

    # 获取查询结果
    users = cur.fetchall()

    # 关闭数据库游标
    cur.close()

    # 通过json对象 返回用户列表数据
    return jsonify({'goods': users}), 200

# 获取用户列表总数
@app.route('/goodsCount',methods=['POST'])
def goodsCount():

    # 获取数据库中用户总数
    cur = connect.cursor()
    cur.execute("SELECT COUNT(*) FROM goodslist")
    count = cur.fetchone()[0]
    # 关闭数据库游标
    cur.close()

    # 通过json对象 返回用户列表总数
    return jsonify({'count': count}), 200