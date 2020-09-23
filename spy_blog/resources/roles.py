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
from schemas.blog import RoleSchema


class RoleResource(Resource):
    """
    角色管理
    """
    def __init__(self):
        self.parser = RequestParser()

    @permission_required
    def get(self):
        '''
        获取全部角色列表
        '''
        # 获取参数
        self.parser.add_argument("offset", type=int, location="args", default=0, help='页码')
        self.parser.add_argument("size", type=int, location="args", default=10, help='每页数量')
        self.parser.add_argument("order_by", type=str, location="args", default='-create_time', help='排序')
        self.args = self.parser.parse_args()
        try:
            roles, total = self.get_roles()
        except Exception as e:
            return pretty_result(http_code.DB_ERROR)
        if roles:
            roles = RoleSchema().dump(roles.all(), many=True)
        return pretty_result(http_code.OK, data={'items': roles, 'total': total})

    def get_roles(self):
        query_obj = Role.query
        total = query_obj.count()
        order_by = self.args.order_by if self.args.order_by else '-create_time'
        order = text(f'-role.{order_by[1:]}') \
            if order_by.startswith('-') else text(f'role.{order_by}')
        return query_obj.order_by(order).offset(self.args.offset).limit(self.args.size), total