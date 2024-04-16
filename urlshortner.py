from flask import Flask, request, redirect, jsonify
import string
import random

app = Flask(__name__)

# Dictionary to store URL mappings
url_mapping = {}

# Characters to use in the short URL
characters = string.ascii_letters + string.digits

# Generate a random short URL code
def generate_short_url():
    length = 6  # Length of the short URL code
    short_url = ''.join(random.choices(characters, k=length))
    return short_url

# Route to shorten a URL
@app.route('/shorten', methods=['POST'])
def shorten_url():
    long_url = request.json.get('url')
    if not long_url:
        return jsonify({'error': 'URL is required'}), 400

    # Check if the URL has already been shortened
    for short_url, url in url_mapping.items():
        if url == long_url:
            return jsonify({'short_url': request.host_url + short_url})

    # Generate a unique short URL code
    short_url = generate_short_url()
    while short_url in url_mapping:
        short_url = generate_short_url()

    # Store the mapping
    url_mapping[short_url] = long_url

    # Return the short URL
    return jsonify({'short_url': request.host_url + short_url})

# Route to redirect short URLs to the long URLs
@app.route('/<short_url>')
def redirect_short_url(short_url):
    if short_url in url_mapping:
        long_url = url_mapping[short_url]
        return redirect(long_url)
    else:
        return jsonify({'error': 'Short URL not found'}), 404

if __name__ == '__main__':
    app.run(port=5000)
