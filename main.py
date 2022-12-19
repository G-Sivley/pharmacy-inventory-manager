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

#TODO: Make drug handling function

def drug_long_name(drug: Drug):
    return f"{drug.name} {drug.measure} {drug.unit}"
    

# Function to find drug in database by ID
def find_drug_by_id(id):
    return Drug.query.filter_by(id=id).first()


@app.route("/")
def home():
    return {"data": 0}


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
    drug_to_remove = find_drug_by_id(drug_id)

    # Check if drug id exists in the database
    if not drug_to_remove:
        return abort(406, "Drug ID not available to delete")

    # Delete drug if it exists
    db.session.delete(drug_to_remove)
    db.session.commit()
    return jsonify("Drug deleted successfully"), 200

# Make add and subtract drug functionality
@app.route("/change-quantity/<int:drug_id>", methods=["POST"])
def change_quantity(drug_id):
    drug_to_change = find_drug_by_id(drug_id)

    # Operation must be "add" or "subtract"
    operation = request.args["operation"]
    print(operation)
    count = int(request.args["count"])

    # Check if drug id exists in database
    if not drug_to_change:
        return abort(406, "Drug ID not available to change")

    # If operation is not add or subtract, provide error
    if operation != "add" and operation != "subtract":
        return abort(406, "Operation is not correct")

    elif operation == "subtract":
        #TODO: Check if drug available to remove
        count *= -1

    # Change and update information
    drug_to_change.count += count
    db.session.commit()
    return jsonify({f"{drug_long_name(drug_to_change)} count changed to": drug_to_change.count}), 200



if __name__ == "__main__":
    app.run(debug=True)