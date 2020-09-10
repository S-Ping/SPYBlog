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
from models.blog import User
from common.decorators import permission_required
from schemas.blog import UserSchema


class UserResource(Resource):
    """
    用户管理
    """
    def __init__(self):
        self.parser = RequestParser()

    @permission_required
    def get(self):
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
        query_obj = None
        if self.args.q:
            query_obj = self.query_users_by_search(self.args.q)
        if query_obj is None:
            query_obj = User.query
        if query_obj:
            total = query_obj.count()
            order = text(f'-user.{self.args.order_by[1:]}') \
                if self.args.order_by.startswith('-') else text(f'user.{self.args.order_by}')
            return query_obj.order_by(order).offset(self.args.offset).limit(self.args.size), total
        return [], 0

    def query_users_by_search(self, q: str):
        query_obj = User.query.filter(
            or_(User.nickname.like(f'%{q}%'), User.email.like(f'%{q}%'))
        )
        return query_obj
