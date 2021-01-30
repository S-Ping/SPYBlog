from models.blog import *
from datetime import datetime



def init_data():
    # 插入权限
    p1 = Permission()
    p1.auth_name = '用户管理'
    p1.desc = '用户管理'
    p1.path = 'user'
    p1.order = 1
    p1.save_to_db()

    p3 = Permission()
    p3.auth_name = '权限管理'
    p3.desc = '角色管理'
    p3.path = 'permission'
    p3.order = 2
    p3.save_to_db()

    p2 = Permission()
    p2.auth_name = '角色列表'
    p2.desc = '角色列表'
    p2.path = 'role'
    p2.order = 1
    p2.parent = p3
    p2.save_to_db()

    p4 = Permission()
    p4.auth_name = '权限列表'
    p4.desc = '角色列表'
    p4.path = 'permission'
    p4.order = 2
    p4.parent = p3
    p4.save_to_db()

    p5 = Permission()
    p5.auth_name = '用户列表'
    p5.desc = '用户列表'
    p5.path = 'user'
    p5.parent = p1
    p5.save_to_db()

    p6 = Permission()
    p6.auth_name = '文章管理'
    p6.desc = '文章管理'
    p6.path = 'article'
    p6.order = 3
    p6.save_to_db()

    p7 = Permission()
    p7.auth_name = '文章列表'
    p7.desc = '文章列表'
    p7.path = 'article'
    p7.order = 1
    p7.parent = p6
    p7.save_to_db()

    p8 = Permission()
    p8.auth_name = '分类列表'
    p8.desc = '分类列表'
    p8.path = 'category'
    p8.order = 2
    p8.parent = p6
    p8.save_to_db()

    p9 = Permission()
    p9.auth_name = '标签列表'
    p9.desc = '标签列表'
    p9.path = 'tag'
    p9.order = 3
    p9.parent = p6
    p9.save_to_db()

    p10 = Permission()
    p10.auth_name = '友链管理'
    p10.desc = '友链管理'
    p10.path = 'friend'
    p10.order = 4
    p10.save_to_db()

    p11 = Permission()
    p11.auth_name = '友链列表'
    p11.desc = '友链列表'
    p11.path = 'friend'
    p11.parent = p10
    p11.save_to_db()

    # 插入角色
    role = Role()
    role.name = '超级管理员'
    role.desc = '拥有所有权限'
    role.permissions = [p1, p2, p3, p4, p5, p6, p7, p8, p9, p10, p11]
    role.save_to_db()

    # 插入标签
    tag = Tag()
    tag.name = 'python'
    tag.save_to_db()

    # 插入分类
    cate = Category()
    cate.category_name = '技术灵感'
    cate.alias = '有技术'
    cate.desc = '做一个有技术有思想的程序员'
    cate.save_to_db()

    # 插入用户
    user = User()
    user.id = 1
    user.email = 'vip@spy.com'
    user.nickname = 'SPY'
    user.last_login = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    user.password = 'spy123456'
    user.signature = '我为SPY抛头颅，洒热血'
    user.roles = [role]
    user.save_to_db()

    # 插入文章内容
    article_body = ArticleBody()
    article_body.content = '# python天下第一'
    article_body.save_to_db()

    # 插入文章
    article = Article()
    article.title = 'python入门'
    article.desc = 'python...'
    article.author_id = 1
    article.view_counts = 10
    article.tags = [tag]
    article.category = cate
    article.body = article_body
    article.save_to_db()

    # 插入文章内容
    article_body = ArticleBody()
    article_body.content = '# python好，python妙'
    article_body.save_to_db()

    # 插入文章
    article = Article()
    article.title = 'python入门2'
    article.desc = '123asd'
    article.author_id = 1
    article.view_counts = 15
    article.tags = [Tag.query.first()]
    article.category_id = 2
    article.body = article_body
    article.save_to_db()


def query_data():
    # 按分类名查找文章
    a = Article.query.join(Article.category).filter(Category.category_name=='技术灵感')
    print(a)
    print('===============================')
    b = Article.query.join(Category).filter(Category.category_name=='技术灵感')
    print(b)
    # 模糊查询
    from sqlalchemy import or_
    a = Article.query.filter(or_(Article.title.like('%py%'), Article.desc.like('%th%')))
    print(a.first())


if __name__ == '__main__':
    from app import create_app
    app = create_app('development')
    with app.app_context():
        # init_data()
        query_data()



