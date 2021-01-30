# 1. api文档  

## 1.1. API  V1接口说明     

- 接口地址: ``

- 服务端已开启 CORS 跨域支持  
- API V1 认证统一使用 Token 认证， 需要授权的 API ，必须在请求头中使用 `Authorization` 字段提供 `token` 令牌  
- 数据返回格式统一使用 JSON  

### 1.1.1.  支持的请求方法    

- GET（SELECT）：从服务器取出资源（一项或多项）。
- POST（CREATE）：在服务器新建一个资源。
- PUT（UPDATE）：在服务器更新资源（客户端提供改变后的完整资源）。
- PATCH（UPDATE）：在服务器更新资源（客户端提供改变的属性）。
- DELETE（DELETE）：从服务器删除资源。  

### 1.1.2. 通用返回状态说明   

| *code* | *含义*                | msg          |
| ------ | --------------------- | ------------ |
| 0      | OK                    | ok           |
| 4001   | DB_ERROR              | 数据库错误   |
| 4002   | DATA_ERROR            | 数据错误     |
| 4003   | PARAM_ERROR           | 请求参数错误 |
| 4004   | AUTHORIZATION_ERROR   | 认证授权错误 |
| 4005   | RATELIMIT_ERROR       | 访问频率过快 |
| 4006   | NOTFOUND_ERROR        | url不存在    |
| 4301   | UNKNOWN_ERROR         | 未知错误     |
| 5001   | INTERNAL_SERVER_ERROR | 内部错误     |

##  

## 1.2. 登录  

### 1.2.1. 登录验证接口  

- 请求路径：auth
- 请求方法：post

- 请求参数  

| 参数名   | 参数说明 | 备注     |
| -------- | -------- | -------- |
| username | 用户名   | 不能为空 |
| password | 密码     | 不能为空 |

- 响应参数   

| 参数名   | 参数说明 | 备注            |
| -------- | -------- | --------------- |
| token    | 令牌     | 基于 jwt 的令牌 |
| nickname | 昵称     |                 |
| email    | 邮箱     |                 |
| avatar   | 头像     |                 |

- 响应数据  

```json
{
    "code": 0,
    "msg": "ok",
    "data": {
        "token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpYXQiOjE2MDQ0NzM3NjIsIm5iZiI6MTYwNDQ3Mz",
        "nickname": "SPY",
        "email": "vip@spy.com",
        "avatar": "https://timgsa.baidu.com/timg?image&quality=80&size=b9999_10000&sec=1599756847846&di=d9389dc4349526336ab7ab94ad4d5466&imgtype=0&"
    }
}
```



### 1.2.2. 获取登录信息  

- 请求路径：auth
- 请求方法：get
- 请求参数：header里面携带token  
- 响应参数：

| 参数名      | 参数说明         | 备注            |
| ----------- | ---------------- | --------------- |
| roles       | 该用户的角色列表 | 基于 jwt 的令牌 |
| nickname    | 昵称             |                 |
| email       | 邮箱             |                 |
| avatar      | 头像             |                 |
| signature   | 个性签名         |                 |
| id          | 唯一ID标识       |                 |
| create_time | 创建时间         |                 |
| lock        | 是否锁定         |                 |
| update_time | 更新时间         |                 |
| last_login  | 上次登录时间     |                 |
| login_addr  | 登录地           |                 |
| login_ip    | 登录IP           |                 |
| is_delete   | 是否删除         |                 |

- 响应数据：

```json
{
    "code": 0,
    "msg": "ok",
    "data": {
        "roles": [
            {
                "id": 4,
                "name": "超级管理员"
            },
            {
                "id": 5,
                "name": "管理员"
            }
        ],
        "nickname": "SPY",
        "signature": "我为SPY抛头颅，洒热血",
        "id": 1,
        "create_time": "2020-09-02T09:25:47",
        "lock": false,
        "update_time": "2020-11-04T15:09:22",
        "last_login": "2020-11-04T15:09:22",
        "avatar": "https://timgsa.baidu.com/timg?image&quality=80&size=b9999_10000&sec=1599756847846&di=d9389dc4349526336ab7ab94ad4d5466&imgtype=0&",
        "login_addr": "local",
        "email": "vip@spy.com",
        "login_ip": "127.0.0.1",
        "is_delete": false
    }
}
```

## 1.3. 菜单管理  

### 1.3.1. 获取菜单列表  

- 请求路径：menu
- 请求方法：get

- 请求参数 ： 携带token

- 响应参数   

| 参数名    | 参数说明   | 备注 |
| --------- | ---------- | ---- |
| icon      | 图标名     |      |
| method    | 请求方法   |      |
| auth_name | 菜单名     |      |
| id        | 唯一ID     |      |
| parent    | 父菜单ID   |      |
| level     | 菜单等级   |      |
| path      | 路径       |      |
| order     | 优先级     |      |
| desc      | 描述       |      |
| children  | 子菜单列表 |      |

- 响应数据  

```json
{
    "code": 0,
    "msg": "ok",
    "data": [
        {
            "icon": "el-icon-s-custom",
            "method": "GET",
            "auth_name": "用户管理",
            "id": 34,
            "parent": null,
            "level": 0,
            "path": "user",
            "order": 1,
            "desc": "用户管理",
            "children": [
                {
                    "icon": "el-icon-s-home",
                    "method": "GET",
                    "auth_name": "用户列表",
                    "id": 38,
                    "parent": 34,
                    "level": 1,
                    "path": "user",
                    "order": null,
                    "desc": "用户列表",
                    "children": [
                        {
                            "icon": "el-icon-s-home",
                            "method": "POST",
                            "auth_name": "添加用户",
                            "id": 45,
                            "parent": 38,
                            "level": 2,
                            "path": "user",
                            "order": 1,
                            "desc": "添加用户",
                            "children": []
                        }
                    ]
                }
            ]
        },
        {
            "icon": "el-icon-lock",
            "method": "GET",
            "auth_name": "权限管理",
            "id": 35,
            "parent": null,
            "level": 0,
            "path": "permission",
            "order": 2,
            "desc": "角色管理",
            "children": [
                {
                    "icon": "el-icon-s-home",
                    "method": "GET",
                    "auth_name": "角色列表",
                    "id": 36,
                    "parent": 35,
                    "level": 1,
                    "path": "role",
                    "order": 1,
                    "desc": "角色列表",
                    "children": [
                        {
                            "icon": "el-icon-s-home",
                            "method": "POST",
                            "auth_name": "添加角色",
                            "id": 49,
                            "parent": 36,
                            "level": 2,
                            "path": "role",
                            "order": 1,
                            "desc": "添加角色",
                            "children": []
                        }
                    ]
                },
                {
                    "icon": "el-icon-s-home",
                    "method": "GET",
                    "auth_name": "权限列表",
                    "id": 37,
                    "parent": 35,
                    "level": 1,
                    "path": "permission",
                    "order": 2,
                    "desc": "权限列表",
                    "children": [
                        {
                            "icon": "el-icon-s-home",
                            "method": "POST",
                            "auth_name": "添加权限",
                            "id": 52,
                            "parent": 37,
                            "level": 2,
                            "path": "permission",
                            "order": 1,
                            "desc": "添加权限",
                            "children": []
                        }
                    ]
                }
            ]
        },
        {
            "icon": "el-icon-document",
            "method": "GET",
            "auth_name": "文章管理",
            "id": 39,
            "parent": null,
            "level": 0,
            "path": "article",
            "order": 3,
            "desc": "文章管理",
            "children": [
                {
                    "icon": "el-icon-s-home",
                    "method": "GET",
                    "auth_name": "文章列表",
                    "id": 40,
                    "parent": 39,
                    "level": 1,
                    "path": "article",
                    "order": 1,
                    "desc": "文章列表",
                    "children": [
                        {
                            "icon": "el-icon-s-home",
                            "method": "POST",
                            "auth_name": "添加文章",
                            "id": 55,
                            "parent": 40,
                            "level": 2,
                            "path": "article",
                            "order": 1,
                            "desc": "添加文章",
                            "children": []
                        }
                    ]
                },
                {
                    "icon": "el-icon-s-home",
                    "method": "GET",
                    "auth_name": "分类列表",
                    "id": 41,
                    "parent": 39,
                    "level": 1,
                    "path": "category",
                    "order": 2,
                    "desc": "分类列表",
                    "children": [
                        {
                            "icon": "el-icon-s-home",
                            "method": "POST",
                            "auth_name": "添加分类",
                            "id": 58,
                            "parent": 41,
                            "level": 2,
                            "path": "category",
                            "order": 1,
                            "desc": "添加分类",
                            "children": []
                        }
                    ]
                },
                {
                    "icon": "el-icon-s-home",
                    "method": "GET",
                    "auth_name": "标签列表",
                    "id": 42,
                    "parent": 39,
                    "level": 1,
                    "path": "tag",
                    "order": 3,
                    "desc": "标签列表",
                    "children": [
                        {
                            "icon": "el-icon-s-home",
                            "method": "POST",
                            "auth_name": "添加标签",
                            "id": 61,
                            "parent": 42,
                            "level": 2,
                            "path": "tag",
                            "order": 1,
                            "desc": "添加标签 ",
                            "children": []
                        }
                    ]
                }
            ]
        },
        {
            "icon": "el-icon-link",
            "method": "GET",
            "auth_name": "友链管理",
            "id": 43,
            "parent": null,
            "level": 0,
            "path": "friend",
            "order": 4,
            "desc": "友链管理",
            "children": [
                {
                    "icon": "el-icon-s-home",
                    "method": "GET",
                    "auth_name": "友链列表",
                    "id": 44,
                    "parent": 43,
                    "level": 1,
                    "path": "friend",
                    "order": null,
                    "desc": "友链列表",
                    "children": [
                        {
                            "icon": "el-icon-s-home",
                            "method": "POST",
                            "auth_name": "添加友情链接",
                            "id": 64,
                            "parent": 44,
                            "level": 2,
                            "path": "friend",
                            "order": 1,
                            "desc": "添加友情链接",
                            "children": []
                        }
                    ]
                }
            ]
        }
    ]
}
```

## 1.4. 用户管理  

### 1.4.1. 新增用户 

- 请求路径：user
- 请求方法：post
- 请求参数：

| 参数名   | 参数说明   | 备注     |
| -------- | ---------- | -------- |
| email    | 邮箱       | 不能为空 |
| nickname | 昵称       | 不能为空 |
| roles    | 角色ID列表 | 不能为空 |

- 响应数据：

```json
{
    "code": 0,
    "msg": "ok",
    "data": null,
}
```

### 1.4.2 获取用户列表  

- 请求路径：user
- 请求方法：get
- 请求参数：

| 参数名   | 参数说明   | 备注               |
| -------- | ---------- | ------------------ |
| offset   | 数据偏移量 | 用于翻页，默认为0  |
| size     | 每页数量   | 默认为10           |
| q        | 搜索       | 默认为空           |
| order_by | 排序       | 默认是-create_time |

- 响应参数：

| 参数名 | 参数说明 | 备注 |
| ------ | -------- | ---- |
| items  | 用户列表 |      |
| total  | 用户总数 |      |

- 响应数据：

```json
{
    "code": 0,
    "msg": "ok",
    "data": {
        "items": [
            {
                "roles": [
                    {
                        "id": 5,
                        "name": "管理员"
                    }
                ],
                "nickname": " 妍经理",
                "signature": "原型图可咋画啊，愁！",
                "id": 3,
                "create_time": "2020-09-10T21:56:07",
                "lock": false,
                "update_time": "2020-09-10T22:06:46",
                "last_login": "2020-09-10T21:56:07",
                "avatar": "https://ss0.bdstatic.com/70cFuHSh_Q1YnxGkpoWK1HF6hhy/it/u=3050041433,3666571347&fm=26&gp=0.jpg",
                "login_addr": "中国，北京",
                "email": "cuixinyan@spy.com",
                "login_ip": null,
                "is_delete": false
            },
            {
                "roles": [
                    {
                        "id": 4,
                        "name": "超级管理员"
                    }
                ],
                "nickname": " 崔董",
                "signature": "为了工作室的美好明天，我们一起加油！",
                "id": 2,
                "create_time": "2020-09-10T21:51:08",
                "lock": false,
                "update_time": "2020-09-10T22:06:12",
                "last_login": "2020-09-10T21:51:08",
                "avatar": "https://timgsa.baidu.com/timg?image&quality=80&size=b9999_10000&sec=1599756768439&di=be6145233fd525d40a1934cddbd7660e&imgtype=0&",
                "login_addr": "中国，北京",
                "email": "cuixinshu@spy.com",
                "login_ip": null,
                "is_delete": false
            },
            {
                "roles": [
                    {
                        "id": 4,
                        "name": "超级管理员"
                    },
                    {
                        "id": 5,
                        "name": "管理员"
                    }
                ],
                "nickname": "SPY",
                "signature": "我为SPY抛头颅，洒热血",
                "id": 1,
                "create_time": "2020-09-02T09:25:47",
                "lock": false,
                "update_time": "2020-11-04T15:09:22",
                "last_login": "2020-11-04T15:09:22",
                "avatar": "https://timgsa.baidu.com/timg?image&quality=80&size=b9999_10000&sec=1599756847846&di=d9389dc4349526336ab7ab94ad4d5466&imgtype=0&",
                "login_addr": "local",
                "email": "vip@spy.com",
                "login_ip": "127.0.0.1",
                "is_delete": false
            }
        ],
        "total": 3
    }
}
```

### 1.4.3. 修改用户 

- 请求路径：user
- 请求方法：put
- 请求参数：
- 响应参数
- 响应数据   

## 1.5. 权限管理  

### 1.5.1. 获取角色列表  

- 请求路径：role
- 请求方法：get
- 请求参数：

| 参数名   | 参数说明   | 备注               |
| -------- | ---------- | ------------------ |
| offset   | 数据偏移量 | 用于翻页，默认为0  |
| size     | 每页数量   | 默认为10           |
| order_by | 排序       | 默认是-create_time |

- 响应参数

| 参数名 | 参数说明 | 备注 |
| ------ | -------- | ---- |
| items  | 角色列表 |      |
| total  | 角色总数 |      |

- 响应数据   

```json
{
    "code": 0,
    "msg": "ok",
    "data": {
        "items": [
            {
                "id": 5,
                "create_time": "2020-09-10T21:59:57",
                "permissions": [
                    {
                        "parent": null,
                        "method": "GET",
                        "id": 39,
                        "path": "article"
                    }
                ],
                "desc": "拥有除用户管理以外的权限",
                "name": "管理员"
            },
            {
                "id": 4,
                "create_time": "2020-09-02T09:25:46",
                "permissions": [
                    {
                        "parent": null,
                        "method": "GET",
                        "id": 34,
                        "path": "user"
                    }
                ],
                "desc": "拥有所有权限",
                "name": "超级管理员"
            }
        ],
        "total": 2
    }
}
```

### 1.5.2. 获取权限列表  

- 请求路径：permission
- 请求方法：get
- 请求参数：

| 参数名 | 参数说明            | 备注     |
| ------ | ------------------- | -------- |
| mode   | 展示形式  tree/list | 默认list |

- 响应数据：

```json
{
    "code": 0,
    "msg": "ok",
    "data": [
        {
            "desc": "用户管理",
            "level": 0,
            "order": 1,
            "path": "user",
            "auth_name": "用户管理",
            "method": "GET",
            "icon": "el-icon-s-custom",
            "id": 34,
            "parent": null
        },
        {
            "desc": "角色管理",
            "level": 0,
            "order": 2,
            "path": "permission",
            "auth_name": "权限管理",
            "method": "GET",
            "icon": "el-icon-lock",
            "id": 35,
            "parent": null
        }
    ]
}
```

## 1.6. 文章管理  

### 1.6.1. 获取文章列表  

- 请求路径：article
- 请求方法：get
- 请求参数：

| 参数名   | 参数说明   | 备注             |
| -------- | ---------- | ---------------- |
| offset   | 数据偏移量 | 用于翻页，默认0  |
| size     | 每页数量   | 默认10           |
| q        | 搜索内容   |                  |
| order_by | 排序       | 默认-create_time |
| category | 文章分类   |                  |
| tag      | 文章标签   |                  |

- 响应参数：

| 参数名 | 参数说明 | 备注 |
| ------ | -------- | ---- |
| items  | 文章列表 |      |
| total  | 文章总数 |      |

- 响应数据：

````json
{
    "code": 0,
    "msg": "ok",
    "data": {
        "items": [
            {
                "desc": "123asd",
                "create_time": "2020-09-03T18:04:23",
                "author": {
                    "nickname": "SPY",
                    "id": 1
                },
                "weight": null,
                "id": 2,
                "publish": true,
                "view_counts": 15,
                "title": "python入门2"
            },
            {
                "desc": "python...",
                "create_time": "2020-09-02T09:25:47",
                "author": {
                    "nickname": "SPY",
                    "id": 1
                },
                "weight": null,
                "id": 1,
                "publish": true,
                "view_counts": 10,
                "title": "python入门"
            }
        ],
        "total": 2
    }
}
````

