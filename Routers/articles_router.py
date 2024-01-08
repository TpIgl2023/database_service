from fastapi import APIRouter, Request, Depends
from sqlalchemy.orm import Session

import Handlers.articles_handlers as articles_handler
from Database.database import get_db
from Models.account_model import Account

articlesRouter = APIRouter()


@articlesRouter.post("/create")
async def create_article(request: Request, db: Session = Depends(get_db)):
    return await articles_handler.create_article_handler(request, db)


@articlesRouter.delete("/delete")
async def delete_article(request: Request, db: Session = Depends(get_db)):
    return articles_handler.delete_article_handler(request, db)


@articlesRouter.put("/update")
async def update_article(request: Request, db: Session = Depends(get_db)):
    return await articles_handler.update_article_handler(request, db)


@articlesRouter.get("/getArticles")
async def get_articles(request: Request, db: Session = Depends(get_db)):
    return await articles_handler.get_articles_handler(request, db)


@articlesRouter.post("/addFavorite")
async def add_favorite(request: Request, db: Session = Depends(get_db)):
    return articles_handler.create_favorite_article_handler(request, db)


@articlesRouter.delete("/removeFavorite")
async def remove_favorite(request: Request, db: Session = Depends(get_db)):
    return articles_handler.delete_favorite_article_handler(request, db)


@articlesRouter.get("/getFavorites")
async def get_favorites(request: Request, db: Session = Depends(get_db)):
    return articles_handler.get_favorite_articles_handler(request, db)


@articlesRouter.get("/getArticlesByIds")
async def get_articles_by_ids(request: Request, db: Session = Depends(get_db)):
    return await articles_handler.get_articles_by_ids_handler(request, db)


@articlesRouter.get("/{article_id}")
async def get_article_by_id(article_id: int, request: Request, db: Session = Depends(get_db)):
    return await articles_handler.get_article_handler(request, article_id, db)




