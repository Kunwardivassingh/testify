from extensions import db

class TestReport(db.Model):
    __tablename__ = 'test_reports'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    source_type = db.Column(db.Enum('upload', 'api'), nullable=False)
    upload_time = db.Column(db.DateTime, default=db.func.current_timestamp())

    # --- NEW COLUMNS TO STORE REPORT METADATA ---
    filename = db.Column(db.String(255), nullable=True)
    filesize = db.Column(db.String(50), nullable=True)
    status = db.Column(db.String(50), default='Completed')

    test_data = db.relationship('TestData', backref='test_report', lazy=True)