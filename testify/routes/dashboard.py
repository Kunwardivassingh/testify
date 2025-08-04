from flask import Blueprint, jsonify, request, redirect, url_for
from extensions import db
from models.test_data import TestData
from sqlalchemy import func

bp = Blueprint('dashboard', __name__, url_prefix='/api/dashboard')

@bp.route('/data')
def get_dashboard_data():
    try:
        query = TestData.query

        start_date = request.args.get('start')
        end_date = request.args.get('end')
        status = request.args.get('status')

        if start_date:
            query = query.filter(TestData.execution_date >= start_date)
        if end_date:
            query = query.filter(TestData.execution_date <= end_date)
        if status and status.lower() != 'all':
            query = query.filter(TestData.status == status)

        data = query.with_entities(
            TestData.id,
            TestData.product_name,
            TestData.test_type,
            TestData.status,
            TestData.execution_date,
            TestData.tester,
            TestData.test_duration
        ).all()

        result = [dict(row._mapping) for row in data]
        return jsonify(result)

    except Exception as e:
        return jsonify({'error': str(e)}), 500

@bp.route('/')
def dashboard_redirect():
    return redirect(url_for('dashboard.data'))  # Redirect to data endpoint or adjust to '/dashboard/' if needed