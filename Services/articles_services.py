from sqlalchemy.orm import Session
from sqlalchemy import and_

from Core.shared import check_field_existence
from Models.article_model import Article
from Models.favorite_model import Favorite
from Models.user_model import User
from datetime import date

PAGE_SIZE = 12


def _check_if_liked(article_id: int, user_id: int, db: Session) -> bool:
    return db.query(Favorite)\
               .filter(
        and_(
            Favorite.article_id == article_id,
            Favorite.user_id == user_id
        )
    ).first() is not None


def create_article(article_json: dict, db: Session):
    with db.begin():
        article = Article.from_dict(article_json)

        db.add(article)
        db.commit()
        db.flush()

    return article.to_dict()


def get_article_by_id(article_id: int, db: Session, user_id: int = None):
    result = db.query(Article).filter(Article.id == article_id)

    if result.first() is None:
        return None

    result_json: dict = result.first().to_dict()

    if user_id is not None:
        result_json.update({
            "isFavorite": _check_if_liked(article_id, user_id, db)
        })

    return result_json


def _build_articles_json_list(articles: list, db: Session, user_id: int = None):
    articles_json = []
    for article in articles:
        article_json = article.to_dict()
        if user_id is not None:
            article_json.update({
                "isFavorite": _check_if_liked(article.id, user_id, db)
            })
        articles_json.append(article_json)

    return articles_json


def get_articles(db: Session, user_id: int = None):
    articles = db.query(Article).order_by(Article.publishDate.desc()).all()

    articles_json = _build_articles_json_list(articles, db, user_id)

    return articles_json


def get_articles_by_page(page: int, db: Session, user_id: int = None):
    articles = db.query(Article).offset(page*PAGE_SIZE).limit(PAGE_SIZE).order_by(Article.publishDate.desc()).all()

    articles_json = _build_articles_json_list(articles, db, user_id=user_id)

    return articles_json


def delete_article(article_id: int, db: Session):
    with db.begin():

        article = db.query(Article).filter(Article.id == article_id).first()

        db.delete(article)

        db.commit()

    return article.to_dict()


def update_article(article_modifications_json: dict, db: Session):

    assert article_modifications_json, "Article modifications not found"
    assert article_modifications_json["id"], "Article id not found"

    with db.begin():
        article = _update_article(article_modifications_json, db)
        db.commit()

    return article.to_dict()


def _update_article(article_modifications_json: dict, db: Session):
    original_account = db.query(Article).filter(Article.id == article_modifications_json["id"]).first()

    assert original_account, "Article not found"

    if check_field_existence(article_modifications_json, "title"):
        original_account.title = article_modifications_json["title"]
    if check_field_existence(article_modifications_json, "resume"):
        original_account.resume = article_modifications_json["resume"]
    if check_field_existence(article_modifications_json, "authors"):
        original_account.authors = "|".join(article_modifications_json["authors"])
    if check_field_existence(article_modifications_json, "institutions"):
        original_account.institutions = "|".join(article_modifications_json["institutions"])
    if check_field_existence(article_modifications_json, "keywords"):
        original_account.keywords = "|".join(article_modifications_json["keywords"])
    if check_field_existence(article_modifications_json, "text"):
        original_account.text = article_modifications_json["text"]
    if check_field_existence(article_modifications_json, "pdfUrl"):
        original_account.pdfUrl = article_modifications_json["pdfUrl"]
    if check_field_existence(article_modifications_json, "references"):
        original_account.references = "|".join(article_modifications_json["references"])
    if check_field_existence(article_modifications_json, "publishDate"):
        original_account.publishDate = date.fromisoformat(article_modifications_json["publishDate"])

    # print(original_account.to_dict())

    return original_account


def create_favorite_article(user_id: int, article_id: int, db: Session):
    with db.begin():

        if db.query(Favorite).filter(Favorite.user_id == user_id, Favorite.article_id == article_id).first() is not None:
            raise Exception("Article already in favorites")

        article = db.query(Article).filter(Article.id == article_id).first()
        user = db.query(User).filter(User.id == user_id).first()

        assert article, "Article not found"
        assert user, "Account not found"

        user.favorite_articles.append(article)

        db.commit()
        db.flush()

    return article.to_dict()


def delete_favorite_article(user_id: int, article_id: int, db: Session):
    with db.begin():

        if db.query(Favorite).filter(Favorite.user_id == user_id, Favorite.article_id == article_id).first() is None:
            raise Exception("Article not in favorites")

        article = db.query(Article).filter(Article.id == article_id).first()
        user = db.query(User).filter(User.id == user_id).first()

        assert article, "Article not found"
        assert user, "Account not found"

        user.favorite_articles.remove(article)

        db.commit()
        db.flush()

    return article.to_dict()


def get_favorite_articles(user_id: int, db: Session):
    user = db.query(User).filter(User.id == user_id).first()

    assert user, "Account not found"

    from operator import attrgetter
    articles_json = []
    for article in sorted(user.favorite_articles, key = attrgetter("publishDate"), reverse=True):
        articles_json.append(article.to_dict())

    return articles_json


def get_favorite_articles_by_page(user_id: int, page: int, db: Session):
    user = db.query(User).filter(User.id == user_id).first()

    assert user, "Account not found"

    favorites = db.query(Favorite).filter(Favorite.user_id == user_id).offset(page*PAGE_SIZE).limit(PAGE_SIZE).all()

    articles_ids = []
    for favorite in favorites:
        articles_ids.append(favorite.article_id)

    articles = db.query(Article).filter(Article.id.in_(articles_ids)).order_by(Article.publishDate.desc()).all()

    articles_json = []
    for article in articles:
        articles_json.append(article.to_dict())

    return articles_json


def get_articles_by_ids(filter_json: dict, db: Session, user_id: int = None):

    articles_filter = _build_articles_filter(filter_json)

    articles = db.query(Article).filter(articles_filter).order_by(Article.publishDate.desc()).all()

    articles_json = _build_articles_json_list(articles, db, user_id=user_id)

    return articles_json


def _build_articles_filter(filter_json):
    account_filter = True

    if check_field_existence(filter_json, "ids"):
        account_filter = and_(account_filter, Article.id.in_(filter_json["ids"]))
    if check_field_existence(filter_json, "publishDate"):
        account_filter = and_(account_filter, Article.publishDate.between(date.fromisoformat(filter_json["publishDate"]["from"]), date.fromisoformat(filter_json["publishDate"]["to"])))
    if check_field_existence(filter_json, "authors"):
        authors = "|".join(filter_json["authors"])
        account_filter = and_(account_filter, Article.authors.like(f"%{authors}%"))
    if check_field_existence(filter_json, "keywords"):
        keywords = "|".join(filter_json["keywords"])
        account_filter = and_(account_filter, Article.keywords.like(f"%{keywords}%"))
    if check_field_existence(filter_json, "references"):
        references = "|".join(filter_json["references"])
        account_filter = and_(account_filter, Article.references.like(f"%{references}%"))
    if check_field_existence(filter_json, "institutions"):
        institutions = "|".join(filter_json["references"])
        account_filter = and_(account_filter, Article.references.like(f"%{institutions}%"))

    return account_filter
