# from flask import Blueprint, request, jsonify, render_template
# from extensions import db
# from models.test_report import TestReport
# from models.test_data import TestData

# bp = Blueprint('upload', __name__, url_prefix='/api')

# @bp.route('/upload', methods=['POST'])
# def upload_data():
#     data = request.get_json()
#     rows = data['rows']
#     user_id = data['user_id']
#     source_type = data['source_type']

#     try:
#         report = TestReport(user_id=user_id, source_type=source_type)
#         db.session.add(report)
#         db.session.flush()
#         report_id = report.id

#         for row in rows:
#             test_data = TestData(
#                 report_id=report_id,
#                 product_name=row['product_name'],
#                 test_id=row['test_id'],
#                 test_type=row['test_type'],
#                 status=row['status'],
#                 execution_date=row['execution_date'],
#                 frequency=row['frequency'],
#                 tester=row['tester'],
#                 test_duration=row['test_duration']
#             )
#             db.session.add(test_data)

#         db.session.commit()
#         return jsonify({'message': 'Data uploaded successfully', 'report_id': report_id})

#     except Exception as err:
#         db.session.rollback()
#         return jsonify({'error': str(err)}), 500

# # New GET route for upload form
# @bp.route('/upload/file', methods=['GET'])
# def upload_file():
#     return render_template('manual_upload.html')


from flask import Blueprint, request, jsonify, render_template
from extensions import db
from models.test_report import TestReport
from models.test_data import TestData

bp = Blueprint('upload', __name__, url_prefix='/api')

@bp.route('/upload', methods=['POST'])
def upload_data():
    data = request.get_json()
    
    # Correctly get the list of rows
    rows = data.get('rows', [])
    user_id = data.get('user_id')
    source_type = data.get('source_type')
    filename = data.get('filename')
    filesize = data.get('filesize')
    
    if not all([rows, user_id, source_type, filename, filesize]):
        return jsonify({'error': 'Missing required data in the request.'}), 400

    try:
        # --- DELETE EXISTING DATA FOR THIS USER ---
        reports_to_delete = TestReport.query.filter_by(user_id=user_id).all()
        for report in reports_to_delete:
            TestData.query.filter_by(report_id=report.id).delete()
            # This line is now correctly uncommented to delete the old report
            # db.session.delete(report)
        
        # --- ADD NEW DATA ---
        report = TestReport(
            user_id=user_id,
            source_type=source_type,
            filename=filename,
            filesize=filesize,
            status='Completed'
        )
        db.session.add(report)
        db.session.flush()
        report_id = report.id

        for row in rows:
            test_data = TestData(
                report_id=report_id,
                product_name=row.get('product_name'),
                test_id=row.get('test_id'),
                test_type=row.get('test_type'),
                status=row.get('status'),
                execution_date=row.get('execution_date'),
                frequency=row.get('frequency'),
                tester=row.get('tester'),
                test_duration=row.get('test_duration')
            )
            db.session.add(test_data)

        db.session.commit()
        return jsonify({'message': 'Data uploaded successfully', 'report_id': report_id})

    except Exception as err:
        db.session.rollback()
        # Provide a more detailed error log for debugging
        print(f"An error occurred: {err}") 
        return jsonify({'error': str(err)}), 500

# New GET route for upload form
@bp.route('/upload/file', methods=['GET'])
def upload_file():
    return render_template('manual_upload.html')