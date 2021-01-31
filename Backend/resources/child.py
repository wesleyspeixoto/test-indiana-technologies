from flask_restful import Resource, reqparse
from models.child import ChildModel
from flask_jwt_extended import jwt_required


attributes = reqparse.RequestParser()
attributes.add_argument('name', type=str)
attributes.add_argument('parents', type=str)


class Child(Resource):
    # /child/{id}
    @jwt_required
    def get(self, id):
        child = ChildModel.find_child(id)
        if child:
            return child.json()
        return {'message': 'Child not found'}, 404


    @jwt_required
    # /child/{id}
    def put(self, id):
        data = attributes.parse_args()
        
        parents_id = list(data['parents'].split(","))

        if len(parents_id) > 2:
            return {"message": "Child cannot have more than 2 Parents"}

        child = ChildModel.find_child(id)
        if child:
            child.update_child(data)
            return {'message': 'Updated child'}
        return {'message': 'Child not found'}, 404


    @jwt_required
    # /child/{id}
    def delete(self, id):
        child = ChildModel.find_child(id)
        if child:
            child.delete_child()
            return {'message': 'Child deleted'}
        return {'message': 'Child not found'}, 404


class CreateChild(Resource):
        #/api/child
    @jwt_required
    def post(self):
        data = attributes.parse_args()
        
        parents_id = list(data['parents'].split(","))
        

        if len(parents_id) > 2:
            return {"message": "Child cannot have more than 2 Parents"}

        child = ChildModel(**data)
        child.save_child()
        return {"message": "Child cread successfully!"}, 201


class Childs(Resource):
    # /api/childs
    @jwt_required
    def get(self):
        childs = ChildModel.childs()
        temp_childs = []
        if childs:
            for child in childs:
                data = {'id': child.id, 'name': child.name, 'child': child.child, 'createdAt': str(child.createdAt), 'updatedAt': str(child.updatedAt)}
                temp_childs.append(data)
            return temp_childs
        return {'message': 'There are no registered childs'}, 404


class ChildUseCase(Resource):
    #/child/{parents}
    @jwt_required
    def get(self, parents):
        childs = ChildModel.childs()
        data = []
        if childs:
            for child in childs:
                if len(child.parents) == parents:
                    data.appen(child)
            return data
        return {'message': 'There are no registered childs'}, 404




