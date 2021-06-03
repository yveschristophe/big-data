# compose_flask/app.py
from flask import Flask
from sqlalchemy import create_engine
from sqlalchemy import text
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import sessionmaker
from flask import jsonify
from sqlalchemy.sql import func

app = Flask(__name__)
engine = create_engine('mysql+pymysql://root:root@db:3306/classicmodels')
Session = sessionmaker(bind=engine)

Base = automap_base()
Base.prepare(engine, reflect=True)

Customer = Base.classes.customers
Employee = Base.classes.employees
Offices = Base.classes.offices
OrderDetail = Base.classes.orderdetails
Order = Base.classes.orders
Payment = Base.classes.payments
ProductLine = Base.classes.productlines
Product = Base.classes.products


@app.route('/')
def hello():
    session = Session()
    result = []
    for instance in session.query(Customer).order_by(Customer.customerNumber):
        result.append(instance.customerName)

    return jsonify(result)


def to_dict(row):
    return {column.name: getattr(row, row.__mapper__.get_property_by_column(column).key) for column in
            row.__table__.columns}


def get_count(q):
    count_q = q.statement.with_only_columns([func.count()]).order_by(None)
    return q.session.execute(count_q).scalar()


@app.route('/count')
def count():
    session = Session()
    r = session.query(func.count(Employee.employeeNumber)).first()
    print(r[0])
    return str(r[0])


@app.route('/1')
def offices():
    session = Session()
    result = []
    for instance in session.query(Offices).order_by(Offices.country, Offices.state, Offices.city):
        result.append(to_dict(instance))
    return jsonify(result)


@app.route('/2')
def total_payments():
    session = Session()
    for instance in session.query(func.sum(Payment.amount)).all():
        return jsonify({'total': str(instance[0])})


@app.route('/3')
def cars():
    session = Session()
    result = []
    for instance in session.query(ProductLine).filter(ProductLine.textDescription.like('%cars%')):
        result.append(to_dict(instance))
    return jsonify(result)


@app.route('/5')
def five():
    session = Session()
    result = []
    for instance in session.query(func.sum(Payment.amount)).filter(Payment.paymentDate == '2004-10-28'):
        return jsonify({'total': str(instance[0])})


@app.route('/6')
def six():
    session = Session()
    result = []
    for instance in session.query(Payment).filter(Payment.amount >= 100000):
        result.append({"amount": str(instance.amount), "checkNumber": instance.checkNumber})
    return jsonify(result)


@app.route('/7')
def seven():
    session = Session()
    result = []
    for instance in session.query(ProductLine).all():
        productLine = {'name': instance.productLine, "products": [], 'count': 0}
        for pinstance in session.query(Product).filter(Product.productLine == instance.productLine):
            productLine["products"].append({"name": pinstance.productName})
        productLine['count'] = len(productLine["products"])
        result.append(productLine)
    return jsonify(result)


@app.route('9')
def nine():
    session = Session()



if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
