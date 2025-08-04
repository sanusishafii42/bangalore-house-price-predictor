from flask import Flask, request, jsonify, send_from_directory  # Import Flask and helpers
import util                                                    # Import your utility functions
import os                                                      # For file path operations

app = Flask(__name__, static_folder='../client/static', template_folder='../client')

@app.route('/get_location_names')
def get_location_names():
    """
    API endpoint to get all available locations for the dropdown.
    """
    response = jsonify({
        'location': util.get_location_names()   # Get locations from util.py
    })
    response.headers.add('Access-Control-Allow-Origin', '*')  # Allow CORS for frontend
    return response
    

@app.route('/predict_home_price', methods=['POST'])
def predict_home_price():
    """
    API endpoint to predict home price based on user input.
    """
    total_sqft = float(request.form['total_sqft'])    # Get total_sqft from form data
    location = request.form['location']               # Get location from form data
    size = int(request.form['size'])                  # Get size (bedrooms) from form data
    bath = int(request.form['bath'])                  # Get bath (bathrooms) from form data
    response = jsonify({
        'estimated_price': util.get_estimated_price(location, total_sqft, size, bath) # Predict price
    })
    return response


@app.route('/')
def home_page():
    return send_from_directory(
        os.path.join(os.path.dirname(__file__), '../client'),
        'index.html'
    )

@app.route('/<path:filename>')
def serve_page(filename):
    # Serve HTML files and static assets
    client_dir = os.path.join(os.path.dirname(__file__), '../client')
    if os.path.exists(os.path.join(client_dir, filename)):
        return send_from_directory(client_dir, filename)
    static_dir = os.path.join(client_dir, 'static')
    if os.path.exists(os.path.join(static_dir, filename)):
        return send_from_directory(static_dir, filename)
    return "Not Found", 404

if __name__ == '__main__':
    util.load_saved_artifact()
    print('Starting Python Flask Server For Home Production....')
    app.run(host='0.0.0.0', port=10000)
    

# @app.route('/')
# def home_page():
#     return send_from_directory(
#         os.path.join(os.path.dirname(__file__), '../client'),
#         'index.html'
#     )

# @app.route('/index.html')
# def index_page():
#     return send_from_directory(
#         os.path.join(os.path.dirname(__file__), '../client'),
#         'index.html'
#     )

# @app.route('/predict.html')
# def predict_page():
#     return send_from_directory(
#         os.path.join(os.path.dirname(__file__), '../client'),
#         'predict.html'
#     )

# @app.route('/contact.html')
# def contact_page():
#     return send_from_directory(
#         os.path.join(os.path.dirname(__file__), '../client'),
#         'contact.html'
#     )

# if __name__ == '__main__':
#     util.load_saved_artifact()                                 # Load model, scaler, and columns
#     print('Starting Python Flask Server For Home Production....')
# app.run(debug=False)                                           # Start Flask server (not in debug mode)