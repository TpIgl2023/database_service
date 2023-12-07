from sqlalchemy import Column, Integer, ForeignKey, Sequence, String
from sqlalchemy.orm import relationship

from Database.database import Base, engine


class Article(Base):

    __tablename__ = "articles"

    id = Column(Integer, Sequence("article_id_seq"), primary_key=True, index=True)
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
            "title": self.title,
            "resume": self.resume,
            "authors": self.authors,
            "keywords": self.keywords,
            "text": self.text,
            "pdfUrl": self.pdfUrl,
            "references": self.references
        }


Base.metadata.create_all(bind=engine)
