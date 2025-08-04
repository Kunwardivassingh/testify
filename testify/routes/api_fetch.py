from flask import Blueprint, render_template

bp = Blueprint('api_fetch', __name__)

@bp.route('/realtime_config', methods=['GET', 'POST'])
def realtime_config():
    return render_template('realtime_config.html')