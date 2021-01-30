from . import db
from .base import BaseModel
from werkzeug.security import generate_password_hash, check_password_hash


# 用戶角色多对多关系表
user_role = db.Table('user_role', db.Model.metadata,
                      db.Column('uid', db.Integer, db.ForeignKey('user.id', ondelete='CASCADE')),
                      db.Column('rid', db.Integer, db.ForeignKey('role.id', ondelete='CASCADE')),
                      db.PrimaryKeyConstraint('uid', 'rid')
                      )


# 角色和权限多对多关系表
role_permission = db.Table('role_permission', db.Model.metadata,
                             db.Column('rid', db.Integer, db.ForeignKey('role.id', ondelete='CASCADE')),
                             db.Column('pid', db.Integer, db.ForeignKey('permission.id', ondelete='CASCADE')),
                             db.PrimaryKeyConstraint('rid', 'pid')
                             )


class Role(db.Model, BaseModel):
    """
    角色表
    """
    __tablename__ = 'role'
    name = db.Column(db.String(32), unique=True, comment='角色名称')
    desc = db.Column(db.String(256), comment='角色描述')
    permissions = db.relationship('Permission', secondary=role_permission, backref=db.backref('roles', lazy='dynamic'))


class User(db.Model, BaseModel):
    """
    用户表
    """
    __tablename__ = 'user'
    email = db.Column(db.String(120), unique=True, comment='邮箱')
    nickname = db.Column(db.String(32), comment='名称')
    pwd = db.Column(db.String(128), comment='密码')
    signature = db.Column(db.String(256), comment='个性签名')
    avatar = db.Column(db.String(512), comment='头像', server_default='https://timgsa.baidu.com/timg?image&quality=80&size=b9999_10000&sec=1600075730122&di=0eb8a83461d4b002d7465e7b67449f38&imgtype=0&src=http%3A%2F%2Fhbimg.b0.upaiyun.com%2Fff4b009e29dc720559674d42595bdd306a494c9ee550-EqxCpY_fw236')
    lock = db.Column(db.BOOLEAN, server_default=db.text('False'), comment='用户锁定')
    last_login = db.Column(db.TIMESTAMP, comment='最近登录时间')
    login_addr = db.Column(db.String(64), comment='登录地址')
    login_ip = db.Column(db.String(16), comment='登录ip')
    articles = db.relationship('Article')
    roles = db.relationship('Role', secondary=user_role, backref=db.backref('users'))

    def __repr__(self):
        return '<User %r>' % self.username

    @property
    def password(self):
        """获取password属性时被调用"""
        raise AttributeError("不可读")

    @password.setter
    def password(self, passwd):
        """设置password属性时被调用，设置密码加密"""
        self.pwd = generate_password_hash(passwd)

    def check_password(self, passwd):
        """检查密码的正确性"""
        return check_password_hash(self.pwd, passwd)


class Permission(db.Model, BaseModel):
    """
    权限表
    """
    __tablename__ = 'permission'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True, comment='主键')
    auth_name = db.Column(db.String(32), comment='权限名称')
    desc = db.Column(db.String(256), comment='权限描述')
    path = db.Column(db.String(32), comment='路由')
    icon = db.Column(db.String(32), server_default='el-icon-s-home', comment='菜单图标')
    order = db.Column(db.Integer, comment='展示顺序')
    level = db.Column(db.Integer, comment='权限等级')
    method = db.Column(db.String(6), server_default='get', comment='请求方法')
    parent_id = db.Column(db.Integer, db.ForeignKey('permission.id'), comment='父级权限id')
    parent = db.relationship('Permission', back_populates='child', remote_side=[id])
    child = db.relationship('Permission', back_populates='parent', cascade='all,delete-orphan')


class Record(db.Model, BaseModel):
    """
    操作日志表
    """
    __tablename__ = 'record'
    module = db.Column(db.String(16), comment='操作模块')
    type = db.Column(db.Integer, nullable=False, comment='操作类型')
    content = db.Column(db.String(256), server_default='-', comment='操作详情')
    create_by = db.Column(db.Integer, comment='操作人id')
    create__by_name = db.Column(db.String(32), comment='操作人名称')


# Create M2M table
# 标签和文章为多对多关系，创建中间表
posts_tags_table = db.Table('article_tag', db.Model.metadata,
                            db.Column('aid', db.Integer, db.ForeignKey('article.id')),
                            db.Column('tid', db.Integer, db.ForeignKey('tag.id')),
                            db.PrimaryKeyConstraint('tid', 'aid')
                            )


class Article(db.Model, BaseModel):
    """
    文章表结构
    """
    __tablename__ = 'article'
    title = db.Column(db.String(64), comment='文章标题')
    desc = db.Column(db.String(500), comment='文章简介')
    author_id = db.Column(db.Integer, db.ForeignKey('user.id'), comment='作者id')
    body_id = db.Column(db.Integer, db.ForeignKey('article_body.id'), unique=True, comment='文章结构体id')
    body = db.relationship('ArticleBody')
    view_counts = db.Column(db.Integer, server_default='0', comment='文章阅读数')
    weight = db.Column(db.Integer, comment='置顶功能')
    publish = db.Column(db.Boolean, server_default=db.text('True'), comment='公开')
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'), comment='分类')
    '''
    # https://stackoverflow.com/questions/36225736/flask-sqlalchemy-paginate-over-objects-in-a-relationship
    # http://www.pythondoc.com/flask-sqlalchemy/models.html#one-to-many
    # https://docs.sqlalchemy.org/en/13/orm/basic_relationships.html#many-to-many
    # https://stackoverflow.com/questions/23469093/flask-sqlalchemy-query-in-a-many-to-many-itself-relationship

    backref 和 lazy 意味着什么了？backref 是一个在 Address 类上声明新属性的简单方法。您也可以使用 my_address.person 来获取使用该地址(address)的人(person)。
    lazy 决定了 SQLAlchemy 什么时候从数据库中加载数据:
    'select' (默认值) 就是说 SQLAlchemy 会使用一个标准的 select 语句必要时一次加载数据。
    'joined' 告诉 SQLAlchemy 使用 JOIN 语句作为父级在同一查询中来加载关系。
    'subquery' 类似 'joined' ，但是 SQLAlchemy 会使用子查询。
    'dynamic' 在有多条数据的时候是特别有用的。不是直接加载这些数据，SQLAlchemy 会返回一个查询对象，在加载数据前您可以过滤（提取）它们。
    您如何为反向引用（backrefs）定义惰性（lazy）状态？使用 backref() 函数:
    '''
    # 注意：dynamic 会每次都进行查询，对性能有影响，不到不得已，不要使用该设置
    tags = db.relationship('Tag', secondary=posts_tags_table, backref=db.backref('articles', lazy='dynamic'),
                           lazy="dynamic")

    author = db.relationship('User', back_populates='articles')
    category = db.relationship('Category', back_populates='articles')
    comments = db.relationship('Comment', back_populates='articles', cascade='all, delete-orphan')

    def __repr__(self):
        return '<Article %r>' % self.title


class Tag(db.Model, BaseModel):
    """
    标签 表结构
    """
    __tablename__ = 'tag'
    name = db.Column(db.String(24), comment='标签名称')
    # articles = db.relationship('Article', secondary=posts_tags_table, backref=db.backref('tags', lazy='dynamic'),
    #                        lazy="dynamic")

    def __repr__(self):
        return '<Tag %r>' % self.tag_name

    def to_json(self):
        data = {'id': self.id,
                'name': self.name
                }
        return data


class ArticleBody(db.Model, BaseModel):
    """
    文章结构体 表结构
    """
    __tablename__ = 'article_body'
    content_html = db.Column(db.Text, comment='文章的html')
    content = db.Column(db.Text, comment='文章内容')

    def __repr__(self):
        return '<ArticleBody %r>' % self.id


class Category(db.Model, BaseModel):
    """
    分类 表结构
    """
    __tablename__ = 'category'
    category_name = db.Column(db.String(32), unique=True, comment='分类名称')
    alias = db.Column(db.String(32), comment='别名')
    desc = db.Column(db.String(255), comment='分类描述')
    articles = db.relationship('Article')

    def __repr__(self):
        return '<Category %r>' % self.category_name


class Comment(db.Model, BaseModel):
    """
    评论表，暂时只建表，不未开发相应功能
    """
    __tablename__ = 'comment'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True, comment='主键')
    author = db.Column(db.String(30), comment='评论者名称')
    email = db.Column(db.String(64), comment='评论者邮箱')
    site = db.Column(db.String(64), comment='评论者网址')
    body = db.Column(db.Text, comment='评论内容')
    from_admin = db.Column(db.Boolean, default=False, comment='来自作者')
    commented_post_id = db.Column(db.Integer, db.ForeignKey('article.id'), comment='评论文章id')
    # 被回复id
    replied_id = db.Column(db.Integer, db.ForeignKey('comment.id'), comment='回复id')
    articles = db.relationship('Article', back_populates='comments')
    # 被回复
    replied = db.relationship('Comment', back_populates='replies', remote_side=[id])
    # 回复的评论
    replies = db.relationship('Comment', back_populates='replied', cascade='all,delete-orphan')


class Friend(db.Model, BaseModel):
    """
    友链 表结构
    """
    __tablename__ = 'friend'
    friend_name = db.Column(db.String(64), comment='好友名称')
    desc = db.Column(db.String(255), comment='好友描述')
    friend_link = db.Column(db.String(64), comment='友链')

    def __repr__(self):
        return '<Friend %r>' % self.friend_name


class Website(db.Model):
    """
    网站访问记录表
    """
    __tablename__ = 'site'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True, comment='主键')
    domain = db.Column(db.String(255))
    url = db.Column(db.String(255))
    title = db.Column(db.String(255), default='')
    ip = db.Column(db.String(255), default='')
    referrer = db.Column(db.String(255), default='')
    user_agent = db.Column(db.String(255), default='')
    headers = db.Column(db.JSON)
    params = db.Column(db.JSON)
    create_time = db.Column(db.TIMESTAMP, server_default=db.text("CURRENT_TIMESTAMP"), comment='创建时间')

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()