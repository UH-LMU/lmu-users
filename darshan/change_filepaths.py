import os
import string
import sys
from sqlalchemy import (create_engine, distinct, MetaData, Table, Column, Integer,
    String, DateTime, Float, ForeignKey, and_, or_, update)
from sqlalchemy.orm import Session
from sqlalchemy.sql import func
from sqlalchemy.ext.automap import automap_base

db = "/input/LMU-active1/harri/Data/Darshan/CellProfiler/DefaultDB_paths.db"
db = "/output/DefaultDB_paths.db"

def newPath(path):
    p = string.replace(path,"/input/","Y:\\\\")
    p = string.replace(p,"/","\\")
    return p

if __name__ == '__main__':
    if not os.path.isfile(db):
        print "db not found"
        sys.exit(1)
        
    engine = create_engine('sqlite:///' + db, echo=False)
    Base = automap_base()
    Base.prepare(engine, reflect=True)
    session = Session(engine)

    # the tables
    image = Base.classes.MyExpt_Per_Image
   
    for i in session.query(image):
        i.Image_PathName_original = newPath(i.Image_PathName_original)
        i.Image_PathName_cellIq = newPath(i.Image_PathName_cellIq)

    session.flush()
    session.commit()
           
