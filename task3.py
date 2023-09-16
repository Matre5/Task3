from flask import Flask, request, json
from flask_restful import Resource, Api, reqparse, marshal_with, fields, abort
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
api = Api(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///persons.db'
db = SQLAlchemy(app)


class PersonM(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    email = db.Column(db.String(50))


# db.create_all()

person_put_args = reqparse.RequestParser()
person_put_args.add_argument("name", type=str, help="Name of the video", required=True)
person_put_args.add_argument("email", type=str, help="Email address required", required=True)
# person_put_args.add_argument("age", type=int, help="Likes on the video")

person_update_args = reqparse.RequestParser()
person_update_args.add_argument("name", type=str, help="Name of the video")
person_update_args.add_argument("email", type=str, help="Email address required")

person_fields = {
    'id': fields.Integer,
    'name': fields.String,
    'email': fields.String
}


class Person(Resource):
    @marshal_with(person_fields)
    def get(self, person_id):
        person = PersonM.query.filter_by(id=person_id).first()
        if not person:
            abort(404, message="Could not find person with that id")
        return person

    @marshal_with(person_fields)
    def put(self, person_id):
        args = person_put_args.parse_args()
        personn = PersonM.query.filter_by(id=person_id).first()
        if personn:
            abort(409, message="id already in use...")
        personn = PersonM()
        db.session.add(personn)
        db.session.commit()
        return personn, 201

    @marshal_with(person_fields)
    def patch(self, person_id):
        args = person_put_args.parse_args()
        person = PersonM.query.filter_by(id=person_id).first()
        if not person:
            abort(404, message="Person doesn't exist to update")
        if args['name']:
            person.name = args['name']
        if args['email']:
            person.email = args['email']

        db.session.commit()

        return person

    def delete(self, person_id):
        person = PersonM.query.get(person_id)
        if person:
            db.session.delete(person)
            db.session.commit()
            return {'message': "Person deleted successfully"}
        return {"Error": "Person does not exist"}


api.add_resource(Person, '/person/<int:person_id>')

if __name__ == '__main__':
    app.run(debug=True)
