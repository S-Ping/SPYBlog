from flask_restful import Resource
from flask_restful.reqparse import RequestParser
from sqlalchemy import or_, text
from flask_jwt_extended import (
    create_access_token,
    jwt_required,
    get_jwt_identity,
    get_jwt_claims
)

from common import http_code, pretty_result
from models.blog import User, Role
from common.decorators import permission_required
from schemas.blog import UserSchema
from libs.mail import check_email, MailSender

from libs.random_str import RandomStr


class UserResource(Resource):
    """
    用户管理
    """
    def __init__(self):
        self.parser = RequestParser()

    @permission_required
    def get(self):
        '''
        获取全部用户列表
        '''
        # 获取参数
        self.parser.add_argument("offset", type=int, location="args", default=0, help='页码')
        self.parser.add_argument("size", type=int, location="args", default=10, help='每页数量')
        self.parser.add_argument("q", type=str, location="args", default='', help='搜索内容', trim=True)
        self.parser.add_argument("order_by", type=str, location="args", default='-create_time', help='排序')
        self.args = self.parser.parse_args()
        try:
            users, total = self.get_users()
        except Exception as e:
            return pretty_result(http_code.DB_ERROR)
        if users:
            users = UserSchema().dump(users.all(), many=True)
        return pretty_result(http_code.OK, data={'items': users, 'total': total})

    def get_users(self):
        '''
        查询用户
        '''
        query_obj = None
        if self.args.q:
            query_obj = self.query_users_by_search(self.args.q)
        if query_obj is None:
            query_obj = User.query
        if query_obj:
            total = query_obj.count()
            order_by = self.args.order_by if self.args.order_by else '-create_time'
            order = text(f'-user.{order_by[1:]}') \
                if order_by.startswith('-') else text(f'user.{order_by}')
            return query_obj.order_by(order).offset(self.args.offset).limit(self.args.size), total
        return [], 0

    def query_users_by_search(self, q: str):
        '''
        搜索用户
        '''
        query_obj = User.query.filter(
            or_(User.nickname.like(f'%{q}%'), User.email.like(f'%{q}%'))
        )
        return query_obj

    def post(self):
        '''
        添加用户
        '''
        self.parser.add_argument("email", type=str, location="json", required=True, help='邮箱', trim=True)
        self.parser.add_argument("nickname", type=str, location="json", required=True, help='昵称', trim=True)
        self.parser.add_argument("roles", type=list, location="json", required=True, help='角色')
        self.args = self.parser.parse_args()
        email = self.args.email
        if not check_email(email):
            return pretty_result(http_code.PARAM_ERROR, '邮箱格式不正确')
        if not self.args.roles:
            return pretty_result(http_code.PARAM_ERROR, '角色不能为空')
        roles = Role.query.filter(Role.id.in_(self.args.roles)).all()
        if not roles:
            return pretty_result(http_code.PARAM_ERROR, '角色不存在')
        pwd = RandomStr().password()
        user = User()
        user.password = pwd
        user.email = email
        user.roles = roles
        user.nickname = self.args.nickname
        try:
            user.save_to_db()
        except Exception as e:
            user.rollback_db()
            return pretty_result(http_code.DB_ERROR)
        else:
            mail = MailSender('开通账户', email)
            mail.html_email('email.html', pwd)
        return pretty_result(http_code.OK)

    def put(self, uid=None):
        self.parser.add_argument("roles", type=list, location="json", help='角色')
        if uid:
            pass
        else:
            uid = get_jwt_identity()
            self.parser.add_argument("nickname", type=str, location="json", help='昵称', trim=True)
