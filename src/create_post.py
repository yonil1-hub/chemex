"""
Handles the creation of post(tutorial)
"""

from flask import Blueprint, jsonify, request
from .database import db, Posts, Users, Comments, Replies
from flask_jwt_extended import get_jwt_identity, jwt_required
import uuid
import re
import os
import subprocess
import bleach
from bs4 import BeautifulSoup

# Create a blueprint for the create route
createPost = Blueprint("create", __name__, url_prefix="/api/v1")

@createPost.route("/create", methods=["POST"])
def create():
    """Create new post
        
        Returns:
                the response of the server.
    """
    # Get form data
    file = request.files['file']
    category = request.form['category']
    title = request.form['title']
    description = request.form['description']
    
    # Validate form data
    if file.filename == '':
        return 'No file selected'
    if not category:
        return 'No category provided'
    if not title:
        return 'No title provided'
    if not description:
        return 'No description provided'

    userId= 1

    # Save the file to a temporary location
    file.save('temp.docx')

    # Define the html variable before the try block
    html = ""
    postno = len(Posts.query.all()) + 1

    # Convert the MS Word document to HTML and extract and rename images from it
    try:
        result = subprocess.run(
            ['pandoc', '-s', 'temp.docx', '-t', 'html', '--extract-media=images/{}'.format(postno)],
            capture_output=True, text=True, check=True
        )
        html = result.stdout
    except subprocess.CalledProcessError as e:
        return jsonify({"msg":"Error converting Word document to HTML: {}".format(e)}), 500

    # Update image names in the HTML document
    image_pattern = r'src="images/image(\d+).jpg"'
    for i, match in enumerate(re.finditer(image_pattern, html)):
        # Generate a new UUID for the image
        image_uuid = str(uuid.uuid4())

        # Replace the old image name with the new UUID in the HTML content
        html = html[:match.start(1)] + image_uuid + html[match.end(1):]

    # Parse the HTML content using BeautifulSoup
    soup = BeautifulSoup(html, 'html.parser')
    body = str(soup.body)

    # Sanitize the HTML content to prevent potential security vulnerabilities
    safe  = bleach.clean(body)

    # Save the post to the database
    try:
        post  = Posts(userId=userId, body=safe, title=title, category=category, description=description)
        db.session.add(post)
        db.session.commit()
    except Exception as e:
        return jsonify({"msg":"Error saving post to database: {}".format(e)})
    return jsonify({"msg":"Post created successfully!"}), 201
