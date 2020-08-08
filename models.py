#necessary imports
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import Column, String, Integer
#from sqlalchemy_imageattach.entity import Image, image_attachment


#database connection
engine = create_engine('postgres://postgres:password@localhost:5432/todore')
Session = sessionmaker(bind=engine)
Base = declarative_base()

#Product model
class Product(Base):
    __tablename__ ='products'


    id = Column(Integer, primary_key = True)
    title = Column(String)
    image_name = Column(String, unique=True)

    def __init__(self,title, image_name):
        self.title = title
        self.image_name= image_name

        
