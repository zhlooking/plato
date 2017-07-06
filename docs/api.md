###     1.1 用户管理
####    1.1.1 添加用户
```
POST /users
{
    username: String,
    email: String,
    password: String,
}

**************************************
201 OK
{
    status: 'success',
    message: '[email] was added!'
}
```
  - 参数说明
    - username          用户名
    - email             邮箱
    - password          设置的密码

  - 返回说明
    - 是否添加成功

###     1.1.2 获取单个用户
```
GET /users/<user_id>
{
    user_id: String
}

**************************************
200 OK
{
    status: 'success',
    data: user
}
```

###     1.1.3 获取全部用户
```
GET /users
{
}

**************************************
200 OK
{
    status: 'success',
    data: [users]
}
```

##      1.2 用户状态管理
###     1.2.1 用户注册
```
POST /auth/register
{
    username: String,
    email: String,
    password: String
}

**************************************
201 OK
{
    status: 'success',
    message: 'Successfully registered',
    auth_token: auth_token
}
```

###     1.2.2 用户登录
```
POST /auth/login
{
    email: String,
    password: String
}

**************************************
201 OK
{
    status: 'success',
    message: 'Successfully logged in',
    auth_token: auth_token
}
```

###     1.2.3 用户退出登录
```
GET /auth/logout
{
}

**************************************
201 OK
{
    status: 'success',
    message: 'Successfully logged out'
}
```

###     1.2.4 查看用户状态
```
GET /auth/status
{
}

**************************************
201 OK
{
    status: 'success',
    data: user
}
```
