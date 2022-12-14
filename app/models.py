from django.db import models
from django.contrib.auth.models import User


class Profile(models.Model):
    nickname = models.CharField(max_length=30)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    email = models.EmailField()
    avatar = models.ImageField()

    def __str__(self):
        return self.nickname


class Tag(models.Model):
    name = models.CharField(max_length=20, unique=True)

    def __str__(self):
        return self.name


class QuestionManager(models.Manager):
    def order_by_date(self):
        return self.order_by('-created')

    def order_by_rating(self):
        return self.order_by('-rating')

    def get_by_tag(self, tag):
        return self.filter(tags__name__icontains=tag)

    def get_by_id(self, id):
        return self.get(pk=id)


class Question(models.Model):
    author = models.ForeignKey(Profile, on_delete=models.CASCADE)
    title = models.CharField(max_length=80)
    text = models.TextField()
    tags = models.ManyToManyField(Tag)
    rating = models.IntegerField(default=0)
    created = models.DateTimeField(auto_now_add=True, editable=False)
    answers = models.IntegerField(default=0)
    objects = QuestionManager()

    def __str__(self):
        return self.title


class AnswerManager(models.Manager):
    def get_answers(self, question):
        return self.filter(question=question)


class Answer(models.Model):
    author = models.ForeignKey(Profile, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    text = models.TextField()
    rating = models.IntegerField(default=0)
    correct = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True, editable=False)
    objects = AnswerManager()


class QuestionGrade(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    value = models.IntegerField()
    user = models.ForeignKey(Profile, on_delete=models.CASCADE)


class AnswerGrade(models.Model):
    answer = models.ForeignKey(Answer, on_delete=models.CASCADE)
    value = models.IntegerField()
    user = models.ForeignKey(Profile, on_delete=models.CASCADE)
