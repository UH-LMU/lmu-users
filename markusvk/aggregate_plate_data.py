from itertools import izip
import numpy
import os
from pprint import pprint
import sys
from sqlalchemy import (create_engine, distinct, MetaData, Table, Column, Integer,
    String, DateTime, Float, ForeignKey, and_, or_)
from sqlalchemy.orm import Session
from sqlalchemy.sql import func
from sqlalchemy.ext.automap import automap_base

db = "/input/LMU-active1/users/vahakosk/CellProfiler/output/DefaultDB.db"
db = "/input/LMU-active1/users/vahakosk/CellProfiler/output/DefaultDB_h1.db"

# http://stackoverflow.com/questions/14180866/sum-each-value-in-a-list-of-tuples
def sums(rows):
    return map(sum,izip(*rows))

def means(rows):
    return map(numpy.mean,izip(*rows))

class WellPlate:
    ROWS = ['A','B','C','D','E','F','G','H']
    COLS = ['01','02','03','04','05','06','07','08','09','10','11','12']
    cols12 = ',,,,,,,,,,,,\n'

    def __init__(self,name):
        self.name = name
        self.measurements = {}


    def addWellMeasurement(self,well,name,value):
        if not name in self.measurements:
            self.measurements[name] = {}
        self.measurements[name][well] = value


    def addWellMeasurements(self,well,names,values,aggregation):
        if len(names) != len(values):
            print "missing name or value", names, values
            sys.exit(1)

        for i in range(1,len(names)+1):
            self.addWellMeasurement(well,names[i],values[i])

    def _printMeasurement(self,key):
        output = '"%s %s",,,,,,,,,,\n'%(self.name,key)
        # add column labels
        output = output + ','
        for c in self.COLS:
            output = output + '"%s",'%c
        output = output + '\n'

        for r in self.ROWS:
            output = output + '"%s",' % r
            values = []
            for c in self.COLS:
                well = r+c
                if well in self.measurements[key]:
                    value = self.measurements[key][well]
                else:
                    value = ""
                values.append(value)
            output = output + '%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s\n'% tuple(values)
        return output
    
    def printout(self):
        for m in sorted(self.measurements):
            #pprint(self.measurements[m])
            print self._printMeasurement(m)
            
        

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
    nuclei = Base.classes.MyExpt_Per_Nuclei
    nucleiGfpPos = Base.classes.MyExpt_Per_GFPpositive
    nucleiGfpNeg = Base.classes.MyExpt_Per_GFPnegative

    # columns for plate and well metadata
    plate = image.Image_Metadata_Plate
    well = image.Image_Metadata_Well

    # data columns of interest
    columnsNuclei = [nuclei.Nuclei_Classify_pos,\
                    nuclei.Nuclei_Classify_neg,\
                    nuclei.Nuclei_Intensity_MeanIntensity_GFP,\
                    nuclei.Nuclei_Children_SpotsLanaBright_Count,\
                    nuclei.Nuclei_Children_SpotsLanaDim_Count]

    columnsNucleiGfp = [nucleiGfpPos.GFPpositive_Intensity_MeanIntensity_MTA,]

    # find unique plate names
    plates = session.query(distinct(plate)).all()
    #print plates
    
    for p in plates:
        p = p[0]
        #print "Plate %s, looking for wells..." % p[0]
        
        # find wells
        wells = session.query(distinct(well)).filter(plate==p).all()
        #print p[0],wells

        wellplate= WellPlate(p)
        for w in wells:
            w = w[0]

            # query nuclei
            queryNuclei = session.query(*columnsNuclei).join(image,nuclei.ImageNumber==image.ImageNumber) \
                          .filter(plate==p,well==w)

            results = queryNuclei.all()
            s = sums(results)
            m = means(results)
            #print w, s, m
            wellplate.addWellMeasurement(w, str(columnsNuclei[0]) + " (number_of_GFP_pos)",s[0])
            wellplate.addWellMeasurement(w, str(columnsNuclei[1]) + " (number_of_GFP_neg)",s[1])
            wellplate.addWellMeasurement(w, "number_of_nuclei",len(results))


            # query Lana positive nuclei
            queryNuclei = session.query(*columnsNuclei).join(image,nuclei.ImageNumber==image.ImageNumber) \
                          .filter(plate==p,well==w)\
                          .filter(or_(columnsNuclei[3]>0,columnsNuclei[4]>0))
            results = queryNuclei.all()
            
            # if no results, there are no positive cells
            nPos = len(results)
            if nPos == 0:
                m = [0,]
            else:
                m = means(results)
            
            wellplate.addWellMeasurement(w, "number_of_Lana_positive",nPos)
            wellplate.addWellMeasurement(w, str(columnsNuclei[3]),m[3])
            wellplate.addWellMeasurement(w, str(columnsNuclei[4]),m[4])

 


            # query GFP positive nuclei
            queryNuclei = session.query(*columnsNucleiGfp).join(image,nucleiGfpPos.ImageNumber==image.ImageNumber) \
                          .filter(plate==p,well==w)
            results = queryNuclei.all()
            
            # if no results, there are no positive cells
            if len(results) == 0:
                m = [0,]
            else:
                m = means(results)
            
            wellplate.addWellMeasurement(w, str(columnsNucleiGfp[0]) + " (average MTA intensity per cell)",m[0])

 
        wellplate.printout()
        #sys.exit()
                                          
        

