from app.utils import choice_interface, search_interface, coming_soon
from database.objects import User, Robot, Article
from ..utils import requires_level
from database.current import get_current_data
from pprint import pprint
import random, time


def view_article(article_id):
    article = Article.get(article_id)
    pprint(article, indent=4)

def all_articles_to_view():
    articles = Article.query()
    get_bot = lambda article: Robot.get(article["author_id"])["name"]
    choice_filter = lambda article: f"{article['title']}: Written by {get_bot(article)}"

    search_interface(
        "View Articles written by robots!",
        search_query=articles, retrieve_func=view_article, choice_filter=choice_filter
    )

def read_article():
    bot = get_current_data("bot")
    articles = Article.query()
    article = random.choice(articles)
    author = Robot.get(article['author_id'])

    print("Finding article to read...")
    time.sleep(2)
    print(f"{bot['name']} is currently reading `{article['title']}` by {author['name']}")
    time.sleep(2)


@requires_level(10)
def write_article():
    bot = get_current_data("bot")


def observe_library():
    choice_interface(
        f"Welcome to the Library!", {
            "View All Articles": all_articles_to_view,
        }
    )

@requires_level(5)
def explore_library():
    bot = get_current_data("bot")
    choice_interface(
        f"Welcome to the Library, {bot['name']}!", {
            "Read Article": read_article,
            "Write Article": write_article
        }
    )
