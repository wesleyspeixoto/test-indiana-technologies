from sql_alchemy import database
from datetime import datetime


class ChildModel(database.Model):
    __tablename__ = "child"

    id = database.Column(database.Integer, primary_key=True)

    name = database.Column(database.String(128))
    parents = database.Column(database.String(256))
    createdAt = database.Column(database.DateTime, nullable=False, default=datetime.utcnow)
    updatedAt = database.Column(database.DateTime, onupdate=datetime.utcnow)


    def __init__(self, name, parents):
        self.name = name
        self.parents = parents
 

    def json(self):
        return {
            'id': self.id,
            'name': self.name,
            'parents': self.parents,
            'createdAt': str(self.createdAt),
            'updatedAt': str(self.updatedAt)
        }


    @classmethod
    def find_child(cls, id):
        child = cls.query.filter_by(id=id).first()
        if child:
            return child
        return None


    @classmethod
    def childs(cls): 
        childs = cls.query.all()
        if childs:
            return childs
        return None


        
    def update_child(self, data):
        if data.name:
            self.name = data.name
        if data.parents:
            self.parents = data.parents
        database.session.commit()


    def save_child(self):
        database.session.add(self)
        database.session.commit()


    def delete_child(self):
        database.session.delete(self)
        database.session.commit()