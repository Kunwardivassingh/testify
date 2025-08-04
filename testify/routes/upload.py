from flask import Blueprint, request, jsonify, render_template
from extensions import db
from models.test_report import TestReport
from models.test_data import TestData

bp = Blueprint('upload', __name__, url_prefix='/api')

@bp.route('/upload', methods=['POST'])
def upload_data():
    data = request.get_json()
    rows = data['rows']
    user_id = data['user_id']
    source_type = data['source_type']

    try:
        report = TestReport(user_id=user_id, source_type=source_type)
        db.session.add(report)
        db.session.flush()
        report_id = report.id

        for row in rows:
            test_data = TestData(
                report_id=report_id,
                product_name=row['product_name'],
                test_id=row['test_id'],
                test_type=row['test_type'],
                status=row['status'],
                execution_date=row['execution_date'],
                frequency=row['frequency'],
                tester=row['tester'],
                test_duration=row['test_duration']
            )
            db.session.add(test_data)

        db.session.commit()
        return jsonify({'message': 'Data uploaded successfully', 'report_id': report_id})

    except Exception as err:
        db.session.rollback()
        return jsonify({'error': str(err)}), 500

# New GET route for upload form
@bp.route('/upload/file', methods=['GET'])
def upload_file():
    return render_template('manual_upload.html')