from flask_restful import Resource, reqparse
from models.parent import ParentModel
from flask_jwt_extended import jwt_required


attributes = reqparse.RequestParser()
attributes.add_argument('name', type=str)
attributes.add_argument('children', type=str)


class Parent(Resource):
    # /parent/{id}
    @jwt_required
    def get(self, id):
        parent = ParentModel.find_parent(id)
        if parent:
            return parent.json()
        return {'message': 'Parent not found'}, 404


    @jwt_required
    # /parent/{id}
    def put(self, id):
        data = attributes.parse_args()
        
        parent = ParentModel.find_parent(id)
        if parent:
            parent.update_parent(data)
            return {'message': 'Updated parent'}
        return {'message': 'Parent not found'}, 404


    @jwt_required
    # /parent/{id}
    def delete(self, id):
        parent = ParentModel.find_parent(id)
        if parent:
            parent.delete_parent()
            return {'message': 'Parent deleted'}
        return {'message': 'Parent not found'}, 404


class CreateParent(Resource):
    #/api/parent
    @jwt_required
    def post(self):
        data = attributes.parse_args()

        parent = ParentModel(**data)
        parent.save_parent()
        return {"message": "Parent cread successfully!"}, 201


class Parents(Resource):
    # /api/parents
    @jwt_required
    def get(self):
        parents = ParentModel.parents()
        temp_parents = []
        if parents:
            for parent in parents:
                data = {'id': parent.id, 'name': parent.name, 'children': parent.children, 'createdAt': str(parent.createdAt), 'updatedAt': str(parent.updatedAt)}
                temp_parents.append(data)
            return temp_parents
        return {'message': 'There are no registered parents'}, 404








