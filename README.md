# Hooda Project - Halal Cart Chatbot

A web-based chatbot that integrates halal cart references into responses for user questions, with location-aware recommendations.

## Features

- Clean, modern web interface inspired by ChatGPT
- Interactive chat experience
- Responses always include halal cart references
- Location-aware recommendations using browser geolocation
- Real-time coordinates display for testing
- Simple Flask-based backend

## Setup and Installation

1. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

2. Set up your OpenAI API key:
   ```
   export OPENAI_API_KEY=your_api_key_here
   ```

3. Run the web application:
   ```
   python app.py
   ```

4. Access the application in your browser at `http://127.0.0.1:8080`

## Usage

1. When you first access the application, your browser will request permission to access your location
2. Grant permission to enable location-aware halal cart recommendations
3. Type your questions or messages in the input field at the bottom of the screen
4. The chatbot will respond with helpful information that always includes references to halal carts near your location
5. Your current coordinates are displayed in the top-right corner of the interface

## Location Data

- The application uses the HTML5 Geolocation API to detect your precise location
- Coordinates are sent in WGS84 format (standard GPS decimal degrees)
- Location data is used only to enhance the AI's responses and is not stored
- The location permission can be revoked through your browser settings at any time