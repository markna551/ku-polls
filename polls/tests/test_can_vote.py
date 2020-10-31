"""Test method and class in ku-polls to use correctly."""
import datetime

from django.test import TestCase
from django.utils import timezone
from polls.models import Question


class QuestionCanVoteTest(TestCase):
    """This class test method can_vote in models.py file."""

    def test_can_vote_question(self):
        """
        can_vote() returns True for questions whose pub_date in the past.

        and end_date in the future.
        """
        pubtime = timezone.now() - datetime.timedelta(days=1, seconds=1)
        endtime = timezone.now() + datetime.timedelta(days=1, seconds=1)
        canvote_question = Question(pub_date=pubtime, end_date=endtime)
        self.assertIs(canvote_question.can_vote(), True)

    def test_can_vote_future_question(self):
        """
        can_vote() returns False for questions whose pub_date in the future.

        and end_date in the future.
        """
        pubtime = timezone.now() + datetime.timedelta(days=3, seconds=1)
        endtime = timezone.now() + datetime.timedelta(days=1, seconds=1)
        canvote_question = Question(pub_date=pubtime, end_date=endtime)
        self.assertIs(canvote_question.can_vote(), False)

    def test_can_vote_ended_question(self):
        """
        can_vote() returns False for questions whose pub_date in the past.

        and end_date in the past.
        """
        pubtime = timezone.now() - datetime.timedelta(days=1, seconds=1)
        endtime = timezone.now() - datetime.timedelta(days=2, seconds=1)
        canvote_question = Question(pub_date=pubtime, end_date=endtime)
        self.assertIs(canvote_question.can_vote(), False)