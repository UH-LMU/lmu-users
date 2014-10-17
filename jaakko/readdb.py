#!/usr/bin/env python

from sqlalchemy import (create_engine, distinct, MetaData, Table, Column, Integer,
        String, DateTime, Float, ForeignKey, and_)
from sqlalchemy.orm import Session
from sqlalchemy.sql import func
from sqlalchemy.ext.automap import automap_base

import math
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
            image.Image_Metadata_Plate, \
            nucleus.nucleus_AreaShape_Center_X,\
            nucleus.nucleus_AreaShape_Center_Y, \
            nucleus.nucleus_Location_Center_X,\
            nucleus.nucleus_Location_Center_Y, \
            anchor.anchor_AreaShape_Center_X,\
            anchor.anchor_AreaShape_Center_Y, \
            anchor.anchor_AreaShape_Orientation]

 
    # find unique plates and average orientation per plate
    plates = session.query(image.Image_Metadata_Plate).distinct()
    avgs = {}
    for p in plates:
        avg = session.query(func.avg(anchor.anchor_AreaShape_Orientation).label('average')) \
                .join(image, image.ImageNumber==anchor.ImageNumber) \
                .filter(image.Image_Metadata_Plate==p[0]) \
                .filter(image.Image_Metadata_QCFlag_multiple_anchors==0) \
                .first()
        #print p[0], avg[0]
        avgs[p[0]] = avg[0]

    # print header row
    #print "'%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s'" % \

    headers = ("image_number","overlay_path","overlay_file","plate", \
            "nucleus_x","nucleus_y","nucleus_com_x","nucleus_com_y",\
            "anchor_x","anchor_y","anchor_angle","anchor_angle_average", \
            "dx_shape","dx_shape_corrected","dx_com","dx_com_corrected")
    fmt = ""
    for h in headers:
        fmt = fmt + "'%s',"

    print fmt % headers

    # find results for images that were not discarded
    query = session.query(*columns) \
            .join(nucleus,image.ImageNumber==nucleus.ImageNumber) \
            .join(anchor,image.ImageNumber==anchor.ImageNumber) \
            .filter(image.Image_Metadata_QCFlag_multiple_anchors==0) \
            .filter(image.Image_Metadata_QCFlag_no_nucleus==0)

    for r in query.all():
        # make a tuple of results
        tr = tuple(r)

        # average anchor orientation for this plate
        ao = avgs[r[3]]

        # distance between nucleus and anchor x-coordinates
        dx = r[8] - r[4]

        # distance between nucleus and anchor center of mass x-coordinates
        dx_com = r[8] - r[6]

        # distances corrected by average anchor orientation
        dx_corr = dx / math.cos(2 * math.pi * ao / 360.0)
        dx_com_corr = dx_com / math.cos(2 * math.pi * ao / 360.0)

        tr = tr + (ao,dx,dx_corr,dx_com,dx_com_corr)

        print "%d,'%s','%s','%s',%d,%d,%d,%d,%d,%d,%f,%f,%d,%f,%d,%f" % tr


    # print empty line
    print ",,,,,,,,,,,,,,,"

    # list discarded images
    query = session.query(*columns) \
            .join(nucleus,image.ImageNumber==nucleus.ImageNumber) \
            .join(anchor,image.ImageNumber==anchor.ImageNumber) \
            .filter(image.Image_Metadata_QCFlag_multiple_anchors==1)
    for r in query.all():
        print "%d,'%s','%s','%s',%d,%d,%d,%d,%d,%d,%f,%s,,,," % (tuple(r) + ("bad anchor",))

    query = session.query(*columns) \
            .join(nucleus,image.ImageNumber==nucleus.ImageNumber) \
            .join(anchor,image.ImageNumber==anchor.ImageNumber) \
            .filter(image.Image_Metadata_QCFlag_no_nucleus==1)
    for r in query.all():
        print "%d,'%s','%s','%s',%d,%d,%d,%d,%d,%d,%f,%s,,,," % (tuple(r) + ("no nucleus",))




