from sqlalchemy.orm import Session

from Models.article_model import Article


def create_article(article_json: dict, db: Session):
    with db.begin():
        article = Article.from_dict(article_json)

        db.add(article)
        db.commit()
        db.flush()

    return article


def get_article_by_id(article_id: int, db: Session):
    return db.query(Article).filter(Article.id == article_id).first().to_dict()


def get_articles(db: Session):
    articles = db.query(Article).all()

    articles_json = []
    for article in articles:
        articles_json.append(article.to_dict())

    return articles_json




