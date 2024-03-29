from fastapi import Request
from sqlalchemy.orm import Session
from starlette.responses import JSONResponse

import Services.articles_services as articles_services
from Core.shared import get_request_body
from Models.article_model import Article


async def create_article_handler(request: Request, db: Session):
    try:

        body = await get_request_body(request)

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


async def get_article_handler(request: Request, article_id: int, db: Session):
    try:

        user_id = None
        if "user_id" in request.headers.keys():
            user_id = int(request.headers.get("user_id"))

        article = articles_services.get_article_by_id(article_id, db, user_id=user_id)
        if article is None:
            return JSONResponse(status_code=404,
                                content={
                                    "message": "Article not found",
                                })
        else:
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
        user_id = None
        if "user_id" in request.headers.keys():
            user_id = int(request.headers.get("user_id"))

        if "page" in request.headers.keys():
            articles = articles_services.get_articles_by_page(int(request.headers.get("page")), db, user_id=user_id)
        else:
            articles = articles_services.get_articles(db, user_id=user_id)

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

        body = await get_request_body(request)
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
            int(request.headers.get("user_id")),
            int(request.headers.get("article_id")),
            db
        )

        return JSONResponse(status_code=200,
                            content={
                                "message": "Favorite article created successfully",
                                "article": article
                            })
    except Exception as e:
        return JSONResponse(status_code=400,
                            content={
                                "message": "Error while creating favorite article",
                                "error": str(e)
                            })


def delete_favorite_article_handler(request: Request, db: Session):
    try:

        article = articles_services.delete_favorite_article(
            int(request.headers.get("user_id")),
            int(request.headers.get("article_id")),
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
            articles = articles_services.get_favorite_articles_by_page(int(request.headers.get("user_id")),
                                                                       int(request.headers.get("page")), db)
        else :
            articles = articles_services.get_favorite_articles(int(request.headers.get("user_id")), db)

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

        body = await get_request_body(request)

        user_id = None
        if "user_id" in request.headers.keys():
            user_id = int(request.headers.get("user_id"))

        articles = articles_services.get_articles_by_ids(body, db, user_id=user_id)

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
