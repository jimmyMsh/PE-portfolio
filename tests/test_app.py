# tests/test_app.py

import unittest
import os
os.environ[ 'TESTING'] = 'true'

from app import app

class AppTestCase(unittest.TestCase):
    def setUp(self):
        self.client = app.test_client()

    def test_home(self):
        response = self.client.get("/")
        assert response.status_code == 200
        html = response.get_data(as_text=True)
        assert '<p class="title">Personal Portfolio</p>' in html
        assert '<h1 class="title">About Me</h1>' in html
        assert 'href="./static/styles/base.css"' in html


    def test_timeline(self):
        response = self.client.get("/api/timeline_post")
        assert response.status_code == 200
        assert response.is_json
        json = response.get_json()
        assert "timeline_posts" in json
        assert len(json["timeline_posts"]) == 0
        # TODO Add more tests relating to the /api/timeline_post GET and POST apis

        # TODO Add more tests relating to the timeline page
    
    def test_timeline_post_get(self):
        # Test POST request to add a new timeline post
        postResponse = self.client.post("/api/timeline_post", data={
            "name": "Inigo Montoya",
            "email": "inigom@example.com",
            "content": "You killed my father, prepare to die."
        })
        assert postResponse.status_code == 200

        # Test that the information of the post is correct
        postJson = postResponse.get_json()
        assert postJson["name"] == "Inigo Montoya"
        assert postJson["email"] == "inigom@example.com"
        assert postJson["content"] == "You killed my father, prepare to die."

        # Test GET request again to ensure post was added
        getResponse = self.client.get("/api/timeline_post")
        assert getResponse.status_code == 200
        assert getResponse.is_json
        json = getResponse.get_json()

        # Test that the information retrieved is correct
        post = json["timeline_posts"][0]
        assert post["name"] == "Inigo Montoya"
        assert post["email"] == "inigom@example.com"
        assert post["content"] == "You killed my father, prepare to die."
    
    # Tests relating to the timeline page
    def test_timeline_page(self):
        response = self.client.get("/timeline")
        assert response.status_code == 200
        html = response.get_data(as_text=True)

        # Testing page's content
        assert '<button class="button is-link" type="submit">Submit</button>' in html
        assert '<label class="label">Name</label>' in html

        # Testing submission form
        formResponse = self.client.post("/api/timeline_post", data={
            "name": "James Bond",
            "email": "jamesb@example.com",
            "content": "The name is Bond, James Bond."
        })
        assert formResponse.status_code == 200

        # Testing that the page show the new post
        response = self.client.get("/timeline")
        assert response.status_code == 200
        html = response.get_data(as_text=True)
        assert "James Bond" in html
        assert "jamesb@example.com" in html
        assert "The name is Bond, James Bond." in html
    
    
    def test_malformed_timeline_post(self):
        # POST request missing name
        response = self.client.post("/api/timeline_post", data= {
            "email": "john@example.com", "content": "Hello world, I'm John!"})
        assert response.status_code == 400
        html = response.get_data(as_text=True)
        assert "Invalid name" in html

        # POST request with empty content
        response = self.client.post("/api/timeline_post", data= {
            "name": "John Doe", "email": "john@example.com", "content":""})
        assert response.status_code == 400
        html = response.get_data(as_text=True)
        assert "Invalid content" in html

        # POST request with malformed email
        response = self.client.post("/api/timeline_post", data= {
            "name": "John Doe", "email": "not-an-email", "content": "Hello world, I'm John!"})
        assert response.status_code == 400
        html = response.get_data(as_text=True)
        assert "Invalid email" in html