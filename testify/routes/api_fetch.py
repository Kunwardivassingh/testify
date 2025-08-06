from flask import Blueprint, render_template, request, jsonify
import pandas as pd

bp = Blueprint('api_fetch', __name__, url_prefix='/api')

@bp.route('/realtime_config')
def realtime_config():
    # This route now just serves the page
    return render_template('realtime_config.html')

# --- NEW: Secure Backend Route to Fetch Live Data ---
@bp.route('/fetch_live_data', methods=['POST'])
def fetch_live_data():
    """
    Receives a URL, fetches the data from it using pandas,
    and returns it as JSON. This bypasses the local database.
    """
    data = request.get_json()
    url = data.get('url')

    if not url:
        return jsonify({"error": "No URL provided"}), 400

    try:
        # Use pandas to directly read the CSV data from the provided URL
        df = pd.read_csv(url)
        
        # Basic validation to ensure it looks like our test data
        expected_columns = ['product_name', 'test_id', 'status']
        if not all(col in df.columns for col in expected_columns):
            return jsonify({"error": "Invalid data format in the provided URL"}), 400

        # Convert the DataFrame to JSON and return it
        return df.to_json(orient='split'), 200

    except Exception as e:
        # Handle errors like invalid URLs, network issues, or incorrect formats
        return jsonify({"error": f"Failed to fetch or parse data: {str(e)}"}), 500
