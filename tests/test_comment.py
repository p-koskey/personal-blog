import unittest
from app.models import Comments
from app import db

def setUp(self):
        
        self.new_comment = Comments(name='Leo',comment='Very good')
        
def tearDown(self):

        Comment.query.delete()
        

def test_check_instance_variables(self):
        self.assertEquals(self.new_comment.name,'Leo')
        self.assertEquals(self.new_comment.comment,'Very Good')


def test_save_post(self):
        self.new_post.save_post()
        self.assertTrue(len(Post.query.all())>0)
