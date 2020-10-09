"""Test method and class in ku-polls to use correctly."""
import datetime
from django.urls import reverse
from django.test import TestCase
from django.utils import timezone
from .models import Question


def create_question(question_text, days, end_days=0):
    """
    Create a question with the given `question_text` ,'days' and end_days.

    Default of end_days = 0.
    """
    time = timezone.now() + datetime.timedelta(days=days)
    end_time = timezone.now() + datetime.timedelta(days=end_days)
    return Question.objects.create(question_text=question_text, pub_date=time, end_date=end_time)


class QuestionIndexViewTests(TestCase):
    """This class test class IndexView in views.py file."""

    def test_no_questions(self):
        """If no question exist, an appropriate message is displayed."""
        response = self.client.get(reverse('polls:index'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "No polls are available")
        self.assertQuerysetEqual(response.context['latest_question_list'], [])

    def test_past_question(self):
        """Questions with a pub_date in the past are displayed on the index page."""
        create_question(question_text="Past question.", days=-30)
        response = self.client.get(reverse('polls:index'))
        self.assertQuerysetEqual(
            response.context['latest_question_list'],
            ['<Question: Past question.>']
        )

    def test_future_question(self):
        """Questions with a pub_date in the future aren't displayed on the index page."""
        create_question(question_text="Future question.", days=30)
        response = self.client.get(reverse('polls:index'))
        self.assertContains(response, "No polls are available.")
        self.assertQuerysetEqual(response.context['latest_question_list'], [])

    def test_future_question_and_past_question(self):
        """Even if both past and future questions exist,only past questions are displayed."""
        create_question(question_text="Past question.", days=-30)
        create_question(question_text="Future question.", days=30)
        response = self.client.get(reverse('polls:index'))
        self.assertQuerysetEqual(
            response.context['latest_question_list'],
            ['<Question: Past question.>']
        )

    def test_two_past_questions(self):
        """The questions index page may display multiple questions."""
        create_question(question_text="Past question 1.", days=-30)
        create_question(question_text="Past question 2.", days=-5)
        response = self.client.get(reverse('polls:index'))
        self.assertQuerysetEqual(
            response.context['latest_question_list'],
            ['<Question: Past question 2.>', '<Question: Past question 1.>'])


class QuestionModelTests(TestCase):
    """This class test method was_published_recently in models.py file."""

    def test_was_published_recently_with_future_question(self):
        """
        was_published_recently() returns False for questions.

        whose pub_date is in the future.
        """
        time = timezone.now() + datetime.timedelta(days=30)
        future_question = Question(pub_date=time)
        self.assertIs(future_question.was_published_recently(), False)

    def test_was_published_recently_with_old_question(self):
        """
        was_published_recently() returns False for questions.

        whose pub_date is older than 1 day.
        """
        time = timezone.now() - datetime.timedelta(days=1, seconds=1)
        old_question = Question(pub_date=time)
        self.assertIs(old_question.was_published_recently(), False)

    def test_was_published_recently_with_recent_question(self):
        """
        was_published_recently() returns True for questions.

        whose pub_date is within the last day.
        """
        time = timezone.now() - datetime.timedelta(
            hours=23, minutes=59, seconds=59)
        recent_question = Question(pub_date=time)
        self.assertIs(recent_question.was_published_recently(), True)


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
