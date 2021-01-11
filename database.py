from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import models


class Database:
    def __init__(self, db_url):
        engine = create_engine(db_url)
        models.Base.metadata.create_all(bind=engine)
        self.session_m = sessionmaker(bind=engine)

    def get_or_create(self, session, model, **data):
        db_model = session.query(model).filter(model.url == data['url']).first()
        if not db_model:
            db_model = model(**data)
        return db_model

    def get_or_create_tag(self, session, model, **tag_data):
        try:
            tag_model = session.query(model).filter(model.tag_url == tag_data['tag_url']).first()
            if not tag_model:
                tag_model = model(**tag_data)
            return tag_model
        except: return

    def create_post(self, data, tag_data):
        session = self.session_m()
        author = self.get_or_create(session, models.Author, **data['author'])
        post = self.get_or_create(session, models.Post, **data['post_data'], author=author)
        session.add(author)
        session.add(post)
        for tag in tag_data:
            tag = self.get_or_create_tag(session, models.Tag, **tag)
            if tag:
                post.tags.append(tag)
                session.add(tag)
        try:
            session.commit()
        except Exception as e:
            print(e)
            session.rollback()
        finally:
            session.close()
    
