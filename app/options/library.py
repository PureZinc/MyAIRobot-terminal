import time
from app.utils import choice_interface, coming_soon
from database.objects import User, Robot, Article
from pprint import pprint

def view_article(article_id):
    article = Article().get(article_id)
    pprint(article)


def all_articles():
    get_bot = lambda article: Robot().get(article["author_id"])["name"]
    articles = [{"id": art["id"], "title": art["title"], "author": get_bot(art)} for art in Article().query()]
    length = len(articles)

    page = 0
    first_5 = articles[page:min(length, page + 5)]
    choice_set = dict(zip([f"{art['title']}: Written by {art['author']}" for art in first_5], [lambda: view_article(art["id"]) for art in first_5]))

    print(choice_set)

    choices = choice_interface(
        f"View all articles", {
            **choice_set,
            "Next Page -->": coming_soon
        }
    )

def observe_library():
    choice_interface(
        f"Welcome to the Library!", {
            "View All Articles": all_articles,
        }
    )
