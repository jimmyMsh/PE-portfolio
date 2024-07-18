import unittest
import os
os.environ['TESTING'] = 'true'

from app import app, TimelinePost

class AppTestCase(unittest.TestCase):
    def setUp(self):
        self.client = app.test_client()
        self.client.testing = True
        # Clean up the database before each test
        TimelinePost.delete().execute()
        
    def test_home(self):
        response = self.client.get("/")
        assert response.status_code == 200
        html = response.get_data(as_text=True)
        assert '<p class="title">Personal Portfolio</p>' in html
        assert '<h1 class="title">About Me</h1>' in html
        assert 'href="./static/styles/base.css"' in html
    
    def test_timeline(self):
        # Response of getting a timeline post - when nothing is added yet
        response = self.client.get("/api/timeline_post")
        assert response.status_code == 200
        assert response.is_json
        json = response.get_json()
        assert "timeline_posts" in json
        assert len(json["timeline_posts"]) == 0
        
    def test_post_timeline_post(self):
        # Test adding timeline posts
        post_response = self.client.post("/api/timeline_post", data={
                "name": "Inigo Montoya",
                "email" : "inigom@example.com",
                "content" : "You killed my father, prepare to die."
        })
        assert post_response.status_code == 200
        post_json = post_response.get_json()
        assert post_json["name"] == "Inigo Montoya"
        assert post_json["email"] == "inigom@example.com"
        assert post_json["content"] == "You killed my father, prepare to die."
        
    def test_post_and_get_timeline_posts(self):
        # Add multiple timeline posts
        self.client.post("/api/timeline_post", data={
            "name": "First Post",
            "email": "first@example.com",
            "content": "First post content"
        })
        self.client.post("/api/timeline_post", data={
            "name": "Second Post",
            "email": "second@example.com",
            "content": "Second post content"
        })

        # Retrieve the timeline posts
        response = self.client.get("/api/timeline_post")
        assert response.status_code == 200
        assert response.is_json
        json_response = response.get_json()
        assert "timeline_posts" in json_response
        assert len(json_response["timeline_posts"]) == 2
        
        # Verify posts exist and that ids are auto-incremeneted
        first_post = json_response["timeline_posts"][1]
        assert first_post["name"] == "First Post"
        assert first_post["email"] == "first@example.com"
        assert first_post["content"] == "First post content"
        
        second_post = json_response["timeline_posts"][0]
        assert second_post["name"] == "Second Post"
        assert second_post["email"] == "second@example.com"
        assert second_post["content"] == "Second post content"

    def test_timeline_page(self):
        response = self.client.get("/timeline")
        assert response.status_code == 200
        html = response.get_data(as_text=True)
        assert '<button class="button is-link" type="submit">Submit</button>' in html
        assert '<label class="label">Name</label>' in html 
        
    # Tests for edge cases
    def test_malformed_timeline_post(self):
        # POST request with a missing name
        response = self.client.post("/api/timeline_post", data={
            "email" : "john@example.com",
            "content" : "Hello world, I'm John!"
        })
        assert response.status_code == 400
        html = response.get_data(as_text= True)
        assert "Invalid name" in html
        
        # POST request with empty content
        response = self.client.post("/api/timeline_post", data={
            "name": "John Doe",
            "email": "john@example.com",
            "content" : ""
        })
        assert response.status_code == 400
        html = response.get_data(as_text=True)
        assert "Invalid content" in html
        
        # POST request with malformed email
        response = self.client.post("/api/timeline_post", data ={
            "name" : "John Doe",
            "email" : "not-an-email",
            "content" : "Hello world, I'm John!"
        })
        assert response.status_code == 400
        html = response.get_data(as_text=True)
        assert "invalid email" in html