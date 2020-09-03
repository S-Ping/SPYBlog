from flask_restful import Resource
from flask_restful.reqparse import RequestParser
from flask_sqlalchemy import BaseQuery
from sqlalchemy import or_, text
from flask_jwt_extended import (
    create_access_token,
    jwt_required,
    get_jwt_identity,
    get_jwt_claims
)

from common import http_code, pretty_result
from models.blog import Article, ArticleBody, Tag
from common.decorators import permission_required
from schemas.blog import ArticleSchema


class UserResource(Resource):
    """
    用户管理
    """
    def __init__(self):
        self.parser = RequestParser()

    @jwt_required
    def get(self):
        # 获取参数
        self.parser.add_argument("offset", type=int, location="args", default=0, help='页码')
        self.parser.add_argument("size", type=int, location="args", default=10, help='每页数量')
        self.parser.add_argument("q", type=str, location="args", default='', help='搜索内容', trim=True)
        self.parser.add_argument("order_by", type=str, location="args", default='-create_time', help='排序')
        self.parser.add_argument("category", type=int, location="args", help='文章分类')
        self.parser.add_argument("tag", type=str, location="args", help='文章标签')
        self.args = self.parser.parse_args()
        try:
            articles, total = self.get_articles()
        except Exception as e:
            return pretty_result(http_code.DB_ERROR)
        if articles:
            articles = ArticleSchema().dump(articles.all(), many=True)
        return pretty_result(http_code.OK, data={'items': articles, 'total': total})

    def get_articles(self):
        query_obj = None
        if self.args.category:
            query_obj = self.query_article_by_category(self.args.category)
        if self.args.tag:
            query_obj = self.query_articles_by_tag(self.args.tag, query_obj)
        if self.args.q:
            query_obj = self.query_articles_by_search(self.args.q, query_obj)
        if query_obj is None:
            query_obj = Article.query
        if query_obj:
            total = query_obj.count()
            order = text(f'-article.{self.args.order_by[1:]}') \
                if self.args.order_by.startswith('-') else text(f'article.{self.args.order_by}')
            return query_obj.order_by(order).offset(self.args.offset).limit(self.args.size), total
        return [], 0

    def query_article_by_category(self, category_id: int):
        return Article.query.filter_by(category_id=category_id)

    def query_articles_by_tag(self, tag: str, query_obj: BaseQuery = None):
        if query_obj is not None:
            query_obj = query_obj.join(Article.tags).filter(Tag.name == tag)
        else:
            query_obj = Article.query.join(Article.tags).filter(Tag.name == tag)
        return query_obj

    def query_articles_by_search(self, q: str, query_obj: BaseQuery = None):
        if query_obj is not None:
            query_obj = query_obj.filter(
                or_(Article.title.like(f'%{q}%'), Article.desc.like(f'%{q}%'))
            )
        else:
            query_obj = Article.query.filter(
                or_(Article.title.like(f'%{q}%'), Article.desc.like(f'%{q}%'))
            )
        return query_obj
