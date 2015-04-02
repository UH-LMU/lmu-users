import csv
import os
import sys
from sqlalchemy import (create_engine, distinct, MetaData, Table, Column, Integer,
    String, DateTime, Float, ForeignKey, and_, or_)
from sqlalchemy.orm import relationship, Session
from sqlalchemy.ext.declarative import declarative_base

db = "/output/DefaultDB_paths.db"
       

if __name__ == '__main__':
    if not os.path.isfile(db):
        print "db not found"
        sys.exit(1)
        
    engine = create_engine('sqlite:///' + db, echo=False)
    Base = declarative_base()
    session = Session(engine)


    class Images(Base):
        __tablename__ = "MyExpt_Per_Image"

        ImageNumber = Column(Integer,primary_key=True)
        Image_PathName_original = Column(String)
        Image_FileName_original = Column(String)

    class Objects(Base):
        __tablename__ = "MyExpt_Per_Object"

        ImageNumber = Column(Integer,primary_key=True)
        ObjectNumber = Column(Integer,primary_key=True)
        cells_AreaShape_Center_X = Column(Float)
        cells_AreaShape_Center_Y = Column(Float)

    class Classes(Base):
        __tablename__ = "per_class"
        ImageNumber = Column(Integer, ForeignKey("MyExpt_Per_Object.ImageNumber"), primary_key=True)
        ObjectNumber = Column(Integer, ForeignKey("MyExpt_Per_Object.ObjectNumber"), primary_key=True)
        class_number = Column(Integer)

        my_object = relationship(Objects,\
                primaryjoin="and_(\
                Classes.ImageNumber==Objects.ImageNumber,\
                Classes.ObjectNumber==Objects.ObjectNumber)")

    # result file
    csvfile = open("test.csv", "w")
    writer = csv.writer(csvfile, quotechar='"', quoting=csv.QUOTE_MINIMAL)

    # find images
    imagelist = session.query(Images)

    for i in imagelist:

        imageinfo = (i.ImageNumber,i.Image_PathName_original,i.Image_FileName_original)

        query = session.query(Objects.cells_AreaShape_Center_X,\
                Objects.cells_AreaShape_Center_Y,\
                Classes.class_number) \
                .join(Classes, and_(\
                Classes.ImageNumber==Objects.ImageNumber,\
                Classes.ObjectNumber==Objects.ObjectNumber) )\
                .filter(Objects.ImageNumber==i.ImageNumber)
        for r in query.all():
            print imageinfo + r
            writer.writerow(imageinfo + r)

        #break

        # slow but works
        # query nuclei
        #objectlist = session.query(Objects)\
        #        .filter(Objects.ImageNumber==i.ImageNumber)

        #for o in objectlist:
        #    c = session.query(Classes)\
        #            .filter(Classes.ImageNumber==i.ImageNumber,Classes.ObjectNumber==o.ObjectNumber).first()

        #    print i.ImageNumber,o.ObjectNumber,c.class_number

    csvfile.close()
