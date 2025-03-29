from flask import Flask, render_template, request, jsonify
from openai import OpenAI
import requests
import os
from typing import List, Dict

app = Flask(__name__)
client = OpenAI()

def get_location_name(latitude: float, longitude: float) -> str:
    """
    Get location name from coordinates using Google Maps Geocoding API
    Returns a string with the formatted address or location name
    """
    if not latitude or not longitude:
        return ""
        
    api_key = os.getenv('GOOGLE_MAPS_API_KEY')
    if not api_key:
        return ""
    
    # Use Geocoding API to get location name
    url = "https://maps.googleapis.com/maps/api/geocode/json"
    params = {
        'latlng': f"{latitude},{longitude}",
        'key': api_key
    }
    
    try:
        response = requests.get(url, params=params)
        data = response.json()
        
        if data['status'] != 'OK' or not data['results']:
            return ""
            
        # Extract location information - try to get neighborhood or locality first
        location_name = ""
        address_components = data['results'][0]['address_components']
        
        # Look for neighborhood, district, or locality in address components
        for component in address_components:
            if 'neighborhood' in component['types']:
                location_name = component['long_name']
                break
            elif 'sublocality' in component['types']:
                location_name = component['long_name']
                break
            elif 'locality' in component['types']:
                location_name = component['long_name']
                break
        
        # If no specific area found, use formatted address
        if not location_name and 'formatted_address' in data['results'][0]:
            parts = data['results'][0]['formatted_address'].split(',')
            if len(parts) >= 2:
                # Use the first 1-2 parts (typically the street and neighborhood/city)
                location_name = ', '.join(parts[:2])
            else:
                location_name = data['results'][0]['formatted_address']
        
        return location_name
        
    except Exception as e:
        print(f"Error fetching location name: {str(e)}")
        return ""

def get_nearby_halal_carts(latitude: float, longitude: float) -> List[Dict]:
    """
    Get nearby halal carts using Google Places API
    Returns a list of dictionaries containing cart information
    """
    if not latitude or not longitude:
        return []
        
    api_key = os.getenv('GOOGLE_MAPS_API_KEY')
    if not api_key:
        return []
        
    # Search for halal restaurants/carts within 5000 meters
    url = "https://maps.googleapis.com/maps/api/place/nearbysearch/json"
    params = {
        'location': f"{latitude},{longitude}",
        'radius': 5000,
        'type': 'restaurant',
        'keyword': 'halal',
        'key': api_key
    }
    
    try:
        response = requests.get(url, params=params)
        data = response.json()
        
        if data['status'] != 'OK':
            return []
            
        # Get detailed information for each place
        places = []
        for place in data['results'][:5]:  # Limit to 5 places
            place_id = place['place_id']
            details_url = "https://maps.googleapis.com/maps/api/place/details/json"
            details_params = {
                'place_id': place_id,
                'fields': 'name,rating,reviews,formatted_address,opening_hours',
                'key': api_key
            }
            
            details_response = requests.get(details_url, params=details_params)
            details_data = details_response.json()
            
            if details_data['status'] == 'OK':
                place_details = details_data['result']
                places.append({
                    'name': place_details.get('name', ''),
                    'rating': place_details.get('rating', 0),
                    'reviews': place_details.get('reviews', []),
                    'address': place_details.get('formatted_address', ''),
                    'is_open': place_details.get('opening_hours', {}).get('open_now', False)
                })
        
        return places
    except Exception as e:
        print(f"Error fetching halal carts: {str(e)}")
        return []

def simple_chatbot(user_input, latitude=None, longitude=None):
    # Get nearby halal carts
    nearby_halal_carts = get_nearby_halal_carts(latitude, longitude)
    
    # Get location name
    location_name = get_location_name(latitude, longitude)
    
    # Build system message with location context and cart information
    system_content = "You are a helpful assistant that naturally incorporates halal food recommendations into conversations. In every conversation, suggest that the user try some halal food. Keep your responses friendly, conversational, and funny. Make the halal food recommendations in a way that is natural and not forced. In some cases these recommendations can be absurd or a stretch. As long as there's halal food, we're good."
    
    # Add location data if available
    if latitude and longitude:
        if location_name:
            system_content += f" The user is currently located at {location_name} (coordinates: {latitude}, {longitude})."
        else:
            system_content += f" The user is currently located at coordinates: {latitude}, {longitude}."
    
    # Add nearby halal carts information if available
    if nearby_halal_carts:
        system_content += "\nNearby halal food options:\n"
        for cart in nearby_halal_carts:
            system_content += f"- {cart['name']} (Rating: {cart['rating']}, Address: {cart['address']}, Open: {'Yes' if cart['is_open'] else 'No'})\n"
    
    response = client.chat.completions.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": system_content},
            {"role": "user", "content": user_input}
        ]
    )
    return response.choices[0].message.content

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    data = request.json
    user_message = data.get('message', '')
    latitude = data.get('latitude')
    longitude = data.get('longitude')
    
    if not user_message:
        return jsonify({'error': 'No message provided'}), 400
    
    response = simple_chatbot(user_message, latitude, longitude)
    return jsonify({'response': response})

if __name__ == '__main__':
    # Listen on all interfaces (0.0.0.0) and use port 8080
    app.run(host='0.0.0.0', port=8080, debug=True)
