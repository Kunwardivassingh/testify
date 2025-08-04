from extensions import db

class TestReport(db.Model):
    __tablename__ = 'test_reports'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    source_type = db.Column(db.Enum('upload', 'api'), nullable=False)
    upload_time = db.Column(db.DateTime, default=db.func.current_timestamp())

    test_data = db.relationship('TestData', backref='test_report', lazy=True)