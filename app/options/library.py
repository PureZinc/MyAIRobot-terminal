from app.utils import choice_interface, search_interface, selection_interface
from database.objects import User, Robot, Article
from ..utils import requires_level
from database.current import get_current_data
from pprint import pprint
import random, time
from services.ai import read_article, generate_article
from ..ai_characters import Leila


def bot_view_article(article_id):
    article = Article.get(article_id)
    pprint(article, indent=4)

def all_articles_to_view():
    articles = Article.query()
    get_bot = lambda article: Robot.get(article["author_id"])["name"]
    choice_filter = lambda article: f"{article['title']}: Written by {get_bot(article)}"

    search_interface(
        "View Articles written by robots!",
        search_query=articles, retrieve_func=bot_view_article, choice_filter=choice_filter
    )

def bot_read_article():
    bot = get_current_data("bot")
    articles = Article.query()
    article = random.choice(articles)
    author = Robot.get(article['author_id'])

    print("Finding article to read...")
    time.sleep(2)
    print(f"{bot['name']} is currently reading `{article['title']}` by {author['name']}")
    review = read_article(bot, article)
    print(review)


@requires_level(8)
def write_article():
    genres = ['science', 'mystery', 'fantasy', 'philosophy', 'history']
    tone = ['joyful', 'neutural', 'persuasive', 'dark']
    bot = get_current_data("bot")
    ask_genre = selection_interface("What Genre would you like?", genres)
    ask_tone = selection_interface("What tone would you like?", tone)
    if any(e == "exited" for e in [ask_genre, ask_tone]): return
    print(f"Genrating a {ask_genre} article of {ask_tone} tone...")

    article, title = generate_article(bot, ask_genre, ask_tone)
    Article.create_article(bot['id'], title=title, content=article)
    Robot.addRobotXP(bot['id'], 120)

def talk_to_leila():
    ask = input("(Press 0 to exit) Ask Leila Anything: ")
    while ask != "0":
        leila_welcome = Leila.generate_response(ask)
        print(leila_welcome)
        ask = input("(Press 0 to exit) Ask Leila Something Else!: ")

def observe_library():
    choice_interface(
        f"Welcome to the Library!", {
            "View All Articles": all_articles_to_view,
            "Talk to Leila": talk_to_leila
        }
    )

@requires_level(5)
def explore_library():
    bot = get_current_data("bot")
    leila_welcome = Leila.generate_response(f"Hi! I'm {bot['name']}!")
    choice_interface(
        leila_welcome, {
            "Read Article": bot_read_article,
            "Write Article": write_article
        }
    )
