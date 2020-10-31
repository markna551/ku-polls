"""Test method and class in ku-polls to use correctly."""
import datetime

from django.test import TestCase
from django.utils import timezone
from polls.models import Question

class QuestionIsPublishedTest(TestCase):
    """This class is test method is_published in models.py file."""

    def test_is_published_question(self):
        """is_published() returns True for questions in the past."""
        pubtime = timezone.now() - datetime.timedelta(days=1, seconds=1)
        published_question = Question(pub_date=pubtime)
        self.assertIs(published_question.is_published(), True)

    def test_is_published_future_question(self):
        """is_published() return False for questions in the future."""
        pubtime = timezone.now() + datetime.timedelta(days=1, seconds=1)
        published_question = Question(pub_date=pubtime)
        self.assertIs(published_question.is_published(), False)