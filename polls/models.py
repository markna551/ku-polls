"""Create Question and Choice to use in ku-polls."""
import datetime
from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

class Question(models.Model):
    """Create question in ku-polls."""

    question_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published')
    end_date = models.DateTimeField('date ended')

    def __str__(self):
        """Return question text."""
        return self.question_text

    def was_published_recently(self):
        """Use to check this polls is published recently."""
        now = timezone.now()
        return now - datetime.timedelta(days=1) <= self.pub_date <= now

    def is_published(self):
        """Use to check this polls is published."""
        now = timezone.now()
        return now >= self.pub_date

    def can_vote(self):
        """Use to check this polls can vote or not."""
        now = timezone.now()
        return self.pub_date <= now <= self.end_date

    was_published_recently.admin_order_field = 'pub_date'
    was_published_recently.boolean = True
    was_published_recently.short_description = 'Published recently?'


class Choice(models.Model):
    """Create choice in ku-polls."""

    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)

    @property
    def votes(self):
        return self.question.vote_set.filter(choice=self).count()

    def __str__(self):
        """Return choice text."""
        return self.choice_text


class Vote(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True,)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice = models.ForeignKey(Choice, on_delete=models.CASCADE)
