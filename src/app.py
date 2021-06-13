
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow

#Conexion a base de datos MYSQL

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root@localhost/kiskodb'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
ma = Marshmallow(app)

class Project(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(70))
    description = db.Column(db.String(100))

    def __init__ (self, name, description):
        self.name = name
        self.description = description

db.create_all()

class ProjectSchema(ma.Schema):
    class Meta:
        fields = ('id', 'name', 'description')

project_schema = ProjectSchema()
projects_schema = ProjectSchema(many=True)

@app.route('/projects', methods=['POST'])

#Metodo Create proyectos
def create_project():
    name = request.json['name']
    description = request.json['description']

    new_project = Project(name, description)
    db.session.add(new_project)
    db.session.commit()

    return project_schema.jsonify(new_project)

#Metodo Read proyectos

#Todos los registros
@app.route('/projects', methods=['GET'])
def get_projects():
    all_projects = Project.query.all()
    result = projects_schema.dump(all_projects)
    return jsonify(result)
#Un solo registro
@app.route('/projects/<id>', methods=['GET'])
def get_project(id):
    project = Project.query.get(id)
    return project_schema.jsonify(project)

#Metodo Update proyectos
@app.route('/projects/<id>', methods=['PUT'])
def update_project(id):
    project = Project.query.get(id)

    name = request.json['name']
    description = request.json['description']

    project.name = name
    project.description = description

    db.session.commit()

    return project_schema.jsonify(project)

#Metodo Delete proyectos
@app.route('/projects/<id>', methods=['DELETE'])
def delete_project(id):
    project = Project.query.get(id)

    db.session.delete(project)
    db.session.commit()

    return project_schema.jsonify(project)


if __name__ == "__main__":
    app.run(debug=True)

