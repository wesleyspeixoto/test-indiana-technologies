from sql_alchemy import database
from datetime import datetime


class ParentModel(database.Model):
    __tablename__ = "parent"

    id = database.Column(database.Integer, primary_key=True)
    
    name = database.Column(database.String(128))
    children = database.Column(database.String(256))
    createdAt = database.Column(database.DateTime, nullable=False, default=datetime.utcnow)
    updatedAt = database.Column(database.DateTime, onupdate=datetime.utcnow)


    def __init__(self, name, children):
        self.name = name
        self.children = children


    def json(self):
        return {
            'id': self.id,
            'name': self.name,
            'children': self.children,
            'createdAt': str(self.createdAt),
            'updatedAt': str(self.updatedAt)
        }


    @classmethod
    def find_parent(cls, id):
        parent = cls.query.filter_by(id=id).first()
        if parent:
            return parent
        return None


    @classmethod
    def parents(cls): 
        parents = cls.query.all()
        if parents:
            return parents
        return None


        
    def update_parent(self, data):
        if data.name:
            self.name = data.name
        if data.children:
            self.children = data.children
        database.session.commit()


    def save_parent(self):
        database.session.add(self)
        database.session.commit()


    def delete_parent(self):
        database.session.delete(self)
        database.session.commit()


