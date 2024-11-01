from app.utils import choice_interface, search_interface, coming_soon
from database.objects import User, Robot, Article
from pprint import pprint

def view_article(article_id):
    article = Article.get(article_id)
    pprint(article, indent=4)


def all_articles():
    articles = Article.query()
    get_bot = lambda article: Robot.get(article["author_id"])["name"]
    choice_filter = lambda article: f"{article['title']}: Written by {get_bot(article)}"

    search_interface(
        "View Articles written by robots!",
        search_query=articles, retrieve_func=view_article, choice_filter=choice_filter
    )

def observe_library():
    choice_interface(
        f"Welcome to the Library!", {
            "View All Articles": all_articles,
        }
    )
