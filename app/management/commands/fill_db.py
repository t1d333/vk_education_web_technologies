from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from app import models
from lorem_text import lorem
import names
import time
import random


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument('ratio', type=int)

    def handle(self, *args, **options):
        ratio = options['ratio']
        profiles = []
        tags = []
        questions = []
        answers = []
        for _ in range(ratio):
            name = names.get_first_name() + str(time.time()).split(".")[1]
            profiles.append(
                models.Profile(
                    nickname=name,
                    email=name + "@test.ru",
                    user=User.objects.create_user(
                        username=name + str(
                            time.time()))))
            tags.append(models.Tag(
                name=(lorem.words(1) + str(time.time()).split(".")[1])[:12]))
        profiles = models.Profile.objects.bulk_create(profiles)
        tags = models.Tag.objects.bulk_create(tags)

        for _ in range(ratio * 10):
            question = models.Question.objects.create(
                author=random.choice(profiles),
                title=lorem.words(3) + "?",
                text=lorem.words(
                    random.choice(
                        range(
                            20,
                            50))),
                rating=0,
                answers=0)
            tags_id = random.choices(range(len(tags)),
                                     k=random.choice(range(1, 4)))

            for id in tags_id:
                question.tags.add(tags[id])
            questions.append(question)

        for _ in range(ratio * 100):
            question_id = random.choice(range(len(questions)))
            questions[question_id].answers += 1
            answer = models.Answer.objects.create(
                author=random.choice(profiles),
                question=questions[question_id],
                text=lorem.words(
                    random.choice(
                        range(
                            20,
                            50))),
                rating=0)
            answers.append(answer)
        models.Question.objects.bulk_update(questions, ['answers'])

        for i in range(ratio * 200):
            if (i % 2 == 0):
                question_id = random.choice(range(len(questions)))
                questions[question_id].rating += ((-1) ** (i % 3))

                models.QuestionGrade.objects.create(user=random.choice(profiles),
                                                    question=questions[question_id],
                                                    value=((-1) ** (i % 3)))
            else:
                answer_id = random.choice(range(len(answers)))
                answers[answer_id].rating += ((-1) ** (i % 3))
                models.AnswerGrade.objects.create(user=random.choice(profiles),
                                                  answer=answers[answer_id],
                                                  value=((-1) ** (i % 3)))

        models.Question.objects.bulk_update(questions, ['rating'])
        models.Answer.objects.bulk_update(answers, ['rating'])
