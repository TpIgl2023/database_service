from sqlalchemy import Column, Integer, ForeignKey, Sequence, String, Date
from sqlalchemy.orm import relationship
from datetime import date

from Database.database import Base, engine


class Article(Base):

    __tablename__ = "articles"

    id = Column(Integer, Sequence("article_id_seq"), primary_key=True, index=True)
    publishDate = Column(Date, nullable=False)
    title = Column(String, nullable=False)
    resume = Column(String, nullable=False)
    authors = Column(String, nullable=False)
    keywords = Column(String, nullable=False)
    text = Column(String, nullable=False)
    pdfUrl = Column(String, nullable=False)
    references = Column(String, nullable=False)

    favorite_by = relationship(
        "User",
        secondary="favorites",
        back_populates="favorite_articles",
    )

    @staticmethod
    def from_dict(article_json: dict):
        return Article(
            publishDate=date.fromisoformat(article_json["publishDate"]),
            title=article_json["title"],
            resume=article_json["resume"],
            authors=article_json["authors"],
            keywords=article_json["keywords"],
            text=article_json["text"],
            pdfUrl=article_json["pdfUrl"],
            references=article_json["references"]
        )

    def to_dict(self):
        return {
            "id": self.id,
            "publishDate": self.publishDate.isoformat(),
            "title": self.title,
            "resume": self.resume,
            "authors": self.authors,
            "keywords": self.keywords,
            "text": self.text,
            "pdfUrl": self.pdfUrl,
            "references": self.references
        }


Base.metadata.create_all(bind=engine)
