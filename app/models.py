from django.db import models

QUESTIONS  = [
    {
        "id": id,
        "title": f'Question #{id}',
        "text": f'Text of question #{id}',
        "answers_count": id + 10,
        "author": f'Author#{id}',
        "creation_date": f'{id + 10} April, 2022',
        "rating": id - 5,
        "tags": ["tag1", "tag2", "tag3"],
        "answers": [
            {
                "rating": ans_id,
                "text": f'Ansewer #{ans_id} for question #{id} ',
                "author": f'Author #{ans_id}',
                "correct": False,
                "creation_date": f'{id + 10} April, 2022',
            } for ans_id in range (3, 300)
            ]
    }for id in range(500)
    
]

HOT_QUESTIONS  = [
    {
        "id": id,
        "title": f'HOT Question #{id}',
        "text": f'Text of hot question #{id}',
        "answers_count": id + 10,
        "author": f'Author#{id}',
        "creation_date": f'{id + 10} April, 2022',
        "rating": id - 5,
        "tags": ["tag1", "tag2", "tag3"],
        "answers": [
            {
                "rating": ans_id,
                "text": f'Ansewer #{ans_id} for question #{id} ',
                "author": f'Author #{ans_id}',
                "correct": False,
                "creation_date": f'{id + 10} April, 2022',
            } for ans_id in range (3, 13)
            ]
    }for id in range(500)
    
]


BEST_MEMBERS = [ f'Best user # {n}'  for n in range(5) ]

TAGS = ["tag1", "tag2", "tag3" ,"perl", "Techopark", "python", "django", "MySql", "Mail.ru", "Firefox", "Techopark"]

POPULAR_TAGS = ["perl", "Techopark", "python", "django", "MySql", "Mail.ru", "Firefox", "Techopark"]
