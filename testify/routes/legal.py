from flask import Blueprint, render_template

bp = Blueprint('legal', __name__)

@bp.route('/privacy-policy')
def privacy_policy():
    """Renders the privacy policy page."""
    return render_template('privacy_policy.html')

@bp.route('/terms-and-conditions')
def terms_and_conditions():
    """Renders the terms and conditions page."""
    return render_template('terms_and_conditions.html')

@bp.route('/contact')
def contact():
    """Renders the contact us page."""
    return render_template('contact.html')