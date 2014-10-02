#!/usr/bin/env python

from sqlalchemy import (create_engine, distinct, MetaData, Table, Column, Integer,
        String, DateTime, Float, ForeignKey, and_)
from sqlalchemy.orm import Session
from sqlalchemy.sql import func
from sqlalchemy.ext.automap import automap_base

import os
import sys

if __name__ == '__main__':
    
    db = sys.argv[1]

    if not os.path.isfile(db):
        print "db not found"
        sys.exit(1)

    engine = create_engine('sqlite:///' + db, echo=False)
    Base = automap_base()
    Base.prepare(engine, reflect=True)
    session = Session(engine)

    # the tables
    image = Base.classes.MyExpt_Per_Image
    nucleus = Base.classes.MyExpt_Per_nucleus
    anchor = Base.classes.MyExpt_Per_anchor
    
    # data columns of interest
    columns = [image.ImageNumber,\
            image.Image_PathName_overlay, \
            image.Image_FileName_overlay, \
            nucleus.nucleus_AreaShape_Center_X,\
            nucleus.nucleus_AreaShape_Center_Y, \
            anchor.anchor_AreaShape_Center_X,\
            anchor.anchor_AreaShape_Center_Y, \
            anchor.anchor_AreaShape_Orientation]

 
    query = session.query(*columns) \
            .join(nucleus,image.ImageNumber==nucleus.ImageNumber) \
            .join(anchor,image.ImageNumber==anchor.ImageNumber)

    results = query.all()

    avg = session.query(func.avg(columns[-1]).label('average')).all()[0][0]

    for r in results:
        print "%d,'%s','%s',%d,%d,%d,%d,%f,%f" % (tuple(r) + (avg,))

