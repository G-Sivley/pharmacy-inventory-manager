from flask import Flask, request, jsonify
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

# Todo: Add checking to ensure not adding same drug
@app.route("/add-drug", methods=["POST"])
def add_drug():
    if request.method == "POST":
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

    return jsonify({"Request completed successfully": 0})
    

# TODO: Make remove drug function

# TODO: Make add quantity drug function

# TODO: Make remove quantity function




if __name__ == "__main__":
    app.run(debug=True)