from flask_restful import Resource
from flask_restful.reqparse import RequestParser
from flask_jwt_extended import (
    create_access_token,
    jwt_required,
    get_jwt_identity,
    get_jwt_claims
)
import datetime

from common import http_code, pretty_result
from models.blog import *
from common.decorators import permission_required
from schemas.blog import RoleSchema


class AuthResource(Resource):
    """
    登录
    """
    def __init__(self):
        self.parser = RequestParser()

    def post(self):
        # 获取参数
        self.parser.add_argument("username", type=str, location="json", required=True)
        self.parser.add_argument("password", type=str, location="json", required=True)
        args = self.parser.parse_args()
        # 查询该邮箱是否存在
        user = User.query.filter(User.email==args.username).first()
        if not user:
            return pretty_result(http_code.DATA_ERROR, msg='用户不存在')
        # 校验密码是否正确
        if not user.check_password(args.password):
            return pretty_result(http_code.DATA_ERROR, msg='用户名或密码错误')
        # 生成token
        timedelta = datetime.timedelta(days=5)
        access_token = create_access_token(identity=user, expires_delta=timedelta)
        return pretty_result(
            http_code.OK,
            data={'token': access_token, 'nickname': user.nickname, 'email': user.email, 'avatar': user.avatar})


class Hello(Resource):
    @permission_required
    def get(self):
        print(123)
        user = User.query.first()
        print(user.roles)
        for i in user.roles:
            print(i.name)
        print(RoleSchema().dump(user.roles, many=True))
        return pretty_result(http_code.OK,data=123)
