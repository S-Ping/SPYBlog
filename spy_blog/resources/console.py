from flask_restful import Resource
from flask_restful.reqparse import RequestParser
from flask_jwt_extended import (
    create_access_token,
    jwt_required,
    get_jwt_identity,
    get_jwt_claims
)

from common import http_code, pretty_result
from models.blog import Permission
from common.decorators import permission_required
from schemas.blog import PermissionSchema


class MenuResource(Resource):
    """
    后台管理菜单列表
    """
    def __init__(self):
        self.parser = RequestParser()

    @jwt_required
    def get(self):
        # 获取token的额外roles参数，在app.py里面设置
        claims = get_jwt_claims()
        roles = claims.get('roles', [])
        pids = []
        for role in roles:
            for permission in role.get('permissions', []):
                if permission['id'] not in pids:
                    pids.append(permission['id'])
        # 查询权限
        permissions = Permission.query.filter(Permission.id.in_(pids))
        self.permissions = PermissionSchema().dump(permissions, many=True)
        # 根据权限生成菜单列表
        self.generate_menu_tree()
        return pretty_result(http_code.OK, data=self.menus)

    def generate_menu_tree(self):
        '''
        生成菜单列表
        :return:
        '''
        # 建立id-node映射表
        id2node_dic = {}
        for node in self.permissions:
            node['children'] = []
            id2node_dic[node['id']] = node
        # 遍历映射表, 将当前节点添加至父节点的children中
        for dir_node in id2node_dic.values():
            if dir_node['parent'] is not None:
                id2node_dic[dir_node['parent']]['children'].append(dir_node)
        self.menus = []
        for node in id2node_dic.values():
            if node['parent'] is None:
                self.menus.append(node)


