from . import db
from sqlalchemy import text, Integer, BOOLEAN, TIMESTAMP


class BaseModel(object):
    """
    数据基础类
    """
    id = db.Column(Integer, primary_key=True, autoincrement=True, comment='主键')
    is_delete = db.Column(BOOLEAN, server_default=text('False'), comment='是否删除')
    create_time = db.Column(TIMESTAMP, server_default=text("CURRENT_TIMESTAMP"), comment='创建时间')
    update_time = db.Column(TIMESTAMP, server_default=text("CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP"), comment='更新时间')

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def commit_to_db(self):
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()