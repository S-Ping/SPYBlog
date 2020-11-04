# -*- coding: utf-8 -*-
from flask import Blueprint
from flask_restful import Api
from resources import profiles, login, console, articles, users, roles

api_v1 = Blueprint('api_v1', __name__)

api = Api(api_v1)

api.add_resource(profiles.ProfileListResource, '/profiles')
api.add_resource(profiles.ProfileResource, '/profiles/<string:id>')
api.add_resource(login.AuthResource, '/auth')
api.add_resource(login.Hello, '/hello')
api.add_resource(console.MenuResource, '/menu')
api.add_resource(articles.ArticleResource, '/article')
api.add_resource(users.UserResource, '/user')
api.add_resource(roles.RoleResource, '/role')
api.add_resource(roles.PermissionResource, '/permission')
