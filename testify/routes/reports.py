from flask import Blueprint, render_template, redirect, url_for,flash
from flask_login import login_required, current_user
from extensions import db
from models.test_report import TestReport
from models.test_data import TestData

bp = Blueprint('reports', __name__)

@bp.route('/reports')
@login_required
def list_reports():
    # Fetch all reports for the current user, ordered by the most recent first
    reports = TestReport.query.filter_by(user_id=current_user.id).order_by(TestReport.upload_time.desc()).all()
    return render_template('reports.html', reports=reports)

# ... (your existing list_reports function) ...

@bp.route('/reports/delete/<int:report_id>', methods=['POST'])
@login_required
def delete_report(report_id):
    # Find the report to delete
    report = TestReport.query.get_or_404(report_id)

    # Security check: ensure the user owns this report
    if report.user_id != current_user.id:
        flash("You do not have permission to delete this report.", "error")
        return redirect(url_for('reports.list_reports'))

    try:
        # Delete all associated test data first
        TestData.query.filter_by(report_id=report.id).delete()
        
        # Delete the report itself
        db.session.delete(report)
        
        # Save the changes to the database
        db.session.commit()
        flash("Report deleted successfully.", "success")
    except Exception as e:
        flash(f"An error occurred while deleting the report: {str(e)}", "error")
    return redirect(url_for('reports.list_reports'))
    return redirect(url_for('reports.list_reports'))