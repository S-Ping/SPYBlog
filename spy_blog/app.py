__author__ = 'SPing'

import os
import string

from flask import Flask, request, abort
from flask_jwt_extended import JWTManager
from flask_marshmallow import Marshmallow
import flask_restful
from hashids import Hashids
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from dotenv import load_dotenv, find_dotenv

from models import db
from config import config
from common import pretty_result, http_code
from libs.flask_logger import register_logger
from libs.redis_cli import redis_store
from schemas import ma
from libs.mail import mail

hash_ids = Hashids(salt='hvwptlmj129d5quf', min_length=8, alphabet=string.ascii_lowercase + string.digits)


def create_app(config_name=None):
    app = Flask(__name__, template_folder='templates', static_folder='static')
    # 加载配置文件
    config_name = os.getenv('FLASK_ENV', 'development')
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)

    # 加载蓝图
    register_blueprint(app)

    # 加载插件
    register_plugin(app)

    return app


def register_blueprint(app):
    '''注册蓝图'''
    from routes import api_v1
    from resources.blue_print import blue
    app.register_blueprint(api_v1, url_prefix='/spy/api/v1')
    app.register_blueprint(blue, url_prefix='/spy')


def register_plugin(app):
    apply_cors(app)  # 应用跨域扩展，使项目支持请求跨域
    handle_error(app)  # 统一处理异常
    db.init_app(app)  # 数据库初始化
    register_logger(__name__)  # 初始化日志
    redis_store.init_app(app)  # 初始化redis
    register_jwt(app)  # 初始化jwt
    register_limiter(app)  # 初始化频率限制
    ma.init_app(app)  # 初始化序列化插件
    mail.init_app(app)  # 初始化邮件插件


    # if app.config['DEBUG']:
    #     apply_request_log(app)  # 打印请求日志


# def apply_json_encoder(app):
#     from libs.json_encoder import JSONEncoder
#     app.json_encoder = JSONEncoder

def custom_abord(http_status_code, *args, **kwargs):
    # 只要http_status_code 为400， 报参数错误
    if http_status_code == 400:
        abort(pretty_result(code=http_code.PARAM_ERROR))
    elif http_status_code == 429:
        abort(pretty_result(code=http_code.RATELIMIT_ERROR))
    # 正常返回消息
    return abort(http_status_code)


def register_jwt(app):
    jwt = JWTManager(app)

    @jwt.user_claims_loader
    def add_claims_to_access_token(user):
        '''
        为token增加额外参数
        :param user:
        :return:
        '''
        from schemas.blog import RoleSchema
        return {
            'email': user.email,
            'nickname': user.nickname,
            'roles': RoleSchema().dump(user.roles, many=True)
        }

    @jwt.user_identity_loader
    def user_identity_lookup(user):
        '''
        用于生成token时可以接收对象
        :param user:
        :return:
        '''
        return user.id

    @jwt.unauthorized_loader
    def missing_token_callback(error):
        return pretty_result(http_code.AUTHORIZATION_ERROR, 'Unauthorized')

    @jwt.expired_token_loader
    def expired_token_callback(error):
        return pretty_result(http_code.AUTHORIZATION_ERROR, 'Expired token')

    @jwt.invalid_token_loader
    def invalid_token_callback(error):
        print(error)
        return pretty_result(http_code.AUTHORIZATION_ERROR, 'Invalid token')


def apply_cors(app):
    # 增加跨域
    from flask_cors import CORS
    cors = CORS()
    cors.init_app(app, resources={"/*": {"origins": "*"}})


def register_limiter(app):
    '''
    访问频率限制
    :param app:
    :return:
    '''
    limiter = Limiter(
        app,
        default_limits=['100/second'],
        key_func=get_remote_address
    )
    limiter.request_filter(filter_func)


def filter_func():
    """
    定义一个限制器的过滤器函数,如果此函数返回True,
    则不会施加任何限制.一般用这个函数创建访问速度
    限制的白名单,可以使用某些celeb集中处理需要
    limiter.exempt的情况
    """
    path_url = request.path
    white_list = ['/exempt']
    if path_url in white_list:
        return True
    else:
        return False


def _access_control(response):
    """
    解决跨域请求
    """
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Methods'] = 'GET,HEAD,PUT,PATCH,POST,DELETE'
    response.headers['Access-Control-Allow-Headers'] = 'Content-Type'
    response.headers['Access-Control-Max-Age'] = 86400
    return response


def handle_error(app):
    '''
    错误处理
    :param app:
    :return:
    '''
    @app.errorhandler(429)
    def ratelimit_error(e):
        return pretty_result(http_code.RATELIMIT_ERROR)

    @app.errorhandler(400)
    def param_error(e):
        return pretty_result(http_code.PARAM_ERROR)

    @app.errorhandler(404)
    def param_error(e):
        return pretty_result(http_code.NOTFOUND_ERROR)

    @app.errorhandler(Exception)
    def framework_error(e):
        print(e)
        if not app.config['DEBUG']:
            return pretty_result(http_code.UNKNOWN_ERROR)  # 未知错误(统一为服务端异常)
        else:
            raise e


# 自定义异常处理
flask_restful.abort = custom_abord
# if __name__ == '__main__':
# #     # load_dotenv(find_dotenv(raise_error_if_not_found=True), override=True, verbose=True)
# #     # print('load...')
# #     # print(os.getenv('FLASK_ENV'))
# #     app = create_app(os.getenv('FLASK_ENV', 'development'))
#     app.run(debug=False, host='0.0.0.0')