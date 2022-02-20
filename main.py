from flask import Flask,jsonify,request,render_template
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import select
import os
from dotenv import load_dotenv
from dataclasses import dataclass
from flask_bootstrap import Bootstrap

load_dotenv()
BASE_URL = os.getenv('BASE_URL')
app = Flask(__name__)
Bootstrap(app)
dbpath = os.path.dirname(os.path.realpath(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///{0}/database.sqlite3".format(
        dbpath
    )
db = SQLAlchemy(app)


@dataclass
class GoblinCakeSales(db.Model):
    ID: str 
    Product: str 
    Product_Type: str 
    Price_Per: int
    Units_Sold: int
    Quarter: int
    ID = db.Column('id', db.Integer, primary_key=True)
    Product = db.Column(db.String(255))
    Product_Type = db.Column(db.String(255))
    Price_Per = db.Column(db.Integer)
    Units_Sold = db.Column(db.Integer)
    Quarter = db.Column(db.Integer)

    def __init__(self, product, product_type, price_per, units_sold, quarter):
        self.Product = product
        self.Product_Type = product_type
        self.Price_Per = price_per
        self.Units_Sold = units_sold
        self.Quarter = quarter 

db.create_all()



def init_database():
    mock_data = [
        ('Hobgoblin', 'Cake',4,388,1),
        ('Green Goblin', 'Cake',4,312,1),
        ('Forest Sprite', 'Canned Drink',0.8,97,1),
        ('Redcap', 'Cake',3.5,605,1),
        ('Imp', 'Cake',2,162,1),

        ('Hobgoblin', 'Cake',4,482,2),
        ('Green Goblin', 'Cake',4,312,2),
        ('Forest Sprite', 'Canned Drink',0.8,123,2),
        ('Redcap', 'Cake',4,401,2),
        ('Imp', 'Cake',1.5,540,2),
        ('Filthy Hobbit', 'Cookie',1,325,2),

        ('Hobgoblin', 'Cake',4,389,3),
        ('Green Goblin', 'Cake',4,302,3),
        ('Forest Sprite', 'Canned Drink',0.8,168,3),
        ('Redcap', 'Cake',4,433,3),
        ('Imp', 'Cake',2,486,3),
        ('Filthy Hobbit', 'Cookie',1,164,3),
        ('Wretched Elf', 'Cookie',1,212,3),
        ('Foul Dwarf', 'Cookie',1,168,3),
        ('Vile Human', 'Cookie',1,92,3),

        ('Hobgoblin', 'Cake',4,369,4),
        ('Green Goblin', 'Cake',4,333,4),
        ('Forest Sprite', 'Canned Drink',0.8,168,4),
        ('Redcap', 'Cake',4,462,4),
        ('Imp', 'Cake',2,501,4),
        ('Filthy Hobbit', 'Cookie',1,125,4),
        ('Wretched Elf', 'Cookie',1,201,4),
        ('Foul Dwarf', 'Cookie',1,162,4),
        ('Vile Human', 'Cookie',1,143,4),
        ('Wizard Spit', 'Hot Drink',3.5,455,4),
        ('Brownie', 'Cake',1.5,666,4)
    ]
    def toMigrationClass(t):
        product, product_type, price_per, units_sold, quarter = t
        return GoblinCakeSales(
            product, 
            product_type, 
            price_per, 
            units_sold, 
            quarter
        )

    #for _ in range(0, 365*20):
    db.session.add_all(map(toMigrationClass, mock_data))
    db.session.commit()

@app.route('/')
def index():
    return render_template("sales.html", baseurl=BASE_URL)

@app.route('/sales/goblin_cakes/<ptype>/<quarter>')
def sales(ptype, quarter):
    sales = db.session.execute(select(GoblinCakeSales).filter(
        GoblinCakeSales.Quarter == quarter, 
        GoblinCakeSales.Product_Type == ptype 
    ))
    return jsonify(list(map(lambda n : n[0], sales)))

if __name__ == '__main__':
    init_database()
    app.run(host="0.0.0.0", port=8000)
