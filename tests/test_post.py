import unittest
from flask_login import current_user
from app.models import Post,User
from app import db

def setUp(self):
        self.user_Kaycee = User(username = 'Kaycee',password = 'potato', email = 'kaycee@ms.com')
        self.new_post = Post(title='Post for movies',content='This movie is the best thing since sliced bread',user = self.user_Kaycee )
def tearDown(self):
        Post.query.delete()
        User.query.delete()

def test_check_instance_variables(self):
        self.assertEquals(self.new_post.title,'Post for movies')
        self.assertEquals(self.new_post.content,'This movie is the best thing since sliced bread')
        self.assertEquals(self.new_post.user,self.user_James)

def test_save_post(self):
        self.new_post.save_post()
        self.assertTrue(len(Post.query.all())>0)
