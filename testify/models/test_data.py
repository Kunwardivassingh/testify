from extensions import db

class TestData(db.Model):
    __tablename__ = 'test_data'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    report_id = db.Column(db.Integer, db.ForeignKey('test_reports.id'), nullable=False)
    product_name = db.Column(db.String(255))
    test_id = db.Column(db.String(100), nullable=False)  # New field for test ID
    test_type = db.Column(db.String(100))
    status = db.Column(db.Enum('Pass', 'Fail', 'Pending'), nullable=False)
    execution_date = db.Column(db.Date)
    frequency = db.Column(db.Integer)
    tester = db.Column(db.String(100))
    test_duration = db.Column(db.Integer)