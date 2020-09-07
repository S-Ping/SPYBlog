from . import ma
from models.blog import User, Role, Permission, Article, ArticleBody, Category, Tag, Comment, Friend, Record
from marshmallow_sqlalchemy import ModelSchema, fields


class UserSchema(ModelSchema):
    roles = fields.Nested('RoleSchema', many=True, only=['id', 'name'])

    class Meta:
        model = User
        exclude = ['articles']


class PermissionSchema(ModelSchema):
    # parent = fields.Nested('PermissionSechma')
    # child = fields.Nested('PermissionSechma', many=True)

    class Meta:
        model = Permission
        exclude = ['roles', 'create_time', 'update_time', 'is_delete', 'child']


class RoleSchema(ModelSchema):
    permissions = fields.Nested('PermissionSchema', many=True, only=['id', 'path', 'method'])

    class Meta:
        model = Role
        fields = ['id', 'name', 'desc', 'permissions', 'create_time']


class ArticleSchema(ModelSchema):

    class Meta:
        model = Article
        fields = ['id', 'title', 'desc', 'weight', 'view_counts', 'create_time']


