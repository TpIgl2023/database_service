from flask import Request
from sqlalchemy.orm import Session
from starlette.responses import JSONResponse

import Services.articles_services as articles_services
from Models.article_model import Article


async def create_article_handler(request: Request, db: Session):
    try:

        body = await request.json()

        article = articles_services.create_article(body, db)

        return JSONResponse(status_code=200,
                            content={
                                "message": "Article created successfully",
                                "article": article
                            })
    except Exception as e:
        return JSONResponse(status_code=400,
                            content={
                                "message": "Error while creating article",
                                "error": str(e)
                            })


async def get_article_handler(article_id: int, db: Session):
    try:

        article = articles_services.get_article_by_id(article_id, db)

        return JSONResponse(status_code=200,
                            content={
                                "message": "Article retrieved successfully",
                                "article": article
                            })
    except Exception as e:
        return JSONResponse(status_code=400,
                            content={
                                "message": "Error while retrieving article",
                                "error": str(e)
                            })


async def get_articles_handler(request: Request, db: Session):
    try:
        if "page" in request.headers.keys():
            articles = articles_services.get_articles_by_page(request.headers.get("page"), db)
        else:
            articles = articles_services.get_articles(db)

        return JSONResponse(status_code=200,
                            content={
                                "message": "Articles retrieved successfully",
                                "articles": articles
                            })
    except Exception as e:
        return JSONResponse(status_code=400,
                            content={
                                "message": "Error while retrieving articles",
                                "error": str(e)
                            })


def delete_article_handler(request: Request, db: Session):
    try:

        article_id = int(request.headers["id"])

        article = articles_services.delete_article(article_id, db)

        return JSONResponse(status_code=200,
                            content={
                                "message": "Article deleted successfully",
                                "article": article
                            })
    except Exception as e:
        return JSONResponse(status_code=400,
                            content={
                                "message": "Error while deleting article",
                                "error": str(e)
                            })


async def update_article_handler(request: Request, db: Session):
    try:
        body = await request.json()

        article = articles_services.update_article(body, db)

        return JSONResponse(status_code=200,
                            content={
                                "message": "Article updated successfully",
                                "article": article
                            })
    except Exception as e:
        return JSONResponse(status_code=400,
                            content={
                                "message": "Error while updating article",
                                "error": str(e)
                            })


def create_favorite_article_handler(request: Request, db: Session):
    try:

        article = articles_services.create_favorite_article(
            request.headers.get("user_id"),
            request.headers.get("article_id"),
            db
        )

        return JSONResponse(status_code=200,
                            content={
                                "message": "Article created successfully",
                                "article": article
                            })
    except Exception as e:
        return JSONResponse(status_code=400,
                            content={
                                "message": "Error while creating article",
                                "error": str(e)
                            })


def delete_favorite_article_handler(request: Request, db: Session):
    try:

        article = articles_services.delete_favorite_article(
            request.headers.get("user_id"),
            request.headers.get("article_id"),
            db
        )

        return JSONResponse(status_code=200,
                            content={
                                "message": "Article deleted successfully",
                                "article": article
                            })
    except Exception as e:
        return JSONResponse(status_code=400,
                            content={
                                "message": "Error while deleting article",
                                "error": str(e)
                            })


def get_favorite_articles_handler(request: Request, db: Session):
    try:
        if "page" in request.headers.keys():
            articles = articles_services.get_favorite_articles_by_page(request.headers.get("user_id"),
                                                                       int(request.headers.get("page")), db)
        else :
            articles = articles_services.get_favorite_articles(request.headers.get("user_id"), db)

        return JSONResponse(status_code=200,
                            content={
                                "message": "Articles retrieved successfully",
                                "articles": articles
                            })
    except Exception as e:
        return JSONResponse(status_code=400,
                            content={
                                "message": "Error while retrieving articles",
                                "error": str(e)
                            })


async def get_articles_by_ids_handler(request: Request, db: Session):
    try:

        body = await request.json()

        articles = articles_services.get_articles_by_ids(body["ids"], db)

        return JSONResponse(status_code=200,
                            content={
                                "message": "Articles retrieved successfully",
                                "articles": articles
                            })
    except Exception as e:
        return JSONResponse(status_code=400,
                            content={
                                "message": "Error while retrieving articles",
                                "error": str(e)
                            })