from flask import Flask, request, jsonify, abort
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# Make database 
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///data.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)

# Make drug object 
class Drug(db.Model):
    __tablename__ = "drugs"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=False)
    measure = db.Column(db.String(50), unique=False)
    unit = db.Column(db.String(25), unique=False)
    count = db.Column(db.Integer)

    # TODO: Check that count is >= 0
    
with app.app_context():
    db.create_all()


@app.route("/")
def home():
    return {"data": 0}


# Todo: Make add drug function

# Add drug to database
# Todo: Add checking to ensure not adding same drug
@app.route("/add-drug", methods=["POST"])
def add_drug():
    name = request.args["drug_name"]
    measure = request.args["measure"]
    unit = request.args["unit"]
    count = int(request.args["count"])
    
    new_drug = Drug(
        name=name,
        measure=measure,
        unit=unit,
        count=count
    )

    db.session.add(new_drug)
    db.session.commit()

    return jsonify({"Request completed successfully": 200})
    

# Make remove drug function
@app.route("/remove-drug/<int:drug_id>", methods=["GET", "POST"])
def remove_drug(drug_id):
    drug_to_remove = Drug.query.filter_by(id=drug_id).first()

    # Check if drug id exists in the database
    if not drug_to_remove:
        return abort(406, "Drug ID not available to delete")

    # Delete drug if it exists
    db.session.delete(drug_to_remove)
    db.session.commit()
    return jsonify("Drug deleted successfully"), 200

# TODO: Make add quantity drug function

# TODO: Make remove quantity function




if __name__ == "__main__":
    app.run(debug=True)