import sqlalchemy
from sqlalchemy import create_engine

#dbpath = "sqlite:////home/hajaalin/tmp/mkhakala/EndocytosisTWF1+2-KO.db"
dbpath = "sqlite:////vagrant/data/EndocytosisTWF1+2-KO.db"
#dbpath = "sqlite:////vagrant/data/EndocytosisTWF1+2-KO_single_object_table.db"

engine = create_engine(dbpath)
conn = engine.connect()

from sqlalchemy import MetaData
m = MetaData()
m.reflect(engine)
# for table in m.tables.values():
#     print("TABLE " + table.name)
#     for column in table.c:
#         print(column.name)
#     print

from sqlalchemy.ext.automap import automap_base
#from sqlalchemy.orm import Session
import sqlalchemy.orm
from sqlalchemy.orm import sessionmaker
from sqlalchemy import and_,Column,ForeignKey,func,Integer,String

Session = sessionmaker(bind=engine)
session = Session()

Base = automap_base()
#Base.prepare(engine, reflect=True)

# class Image(Base):
#     __tablename__ = 'TWFKO_Per_Image'
#
# #Image = Base.classes.TWFKO_Per_Image
# class Cells(Base):
#     __tablename__ = 'TWFKO_Per_Cells'

class Endocytosis(Base):
    __tablename__ = 'TWFKO_Per_Endocytosis'
    # ImageNumber = Column(ForeignKey('TWFKO_Per_Cells.ImageNumber'))
    # Endocytosis_Parent_Cells = Column(ForeignKey('TWFKO_Per_Cells.Cells_Number_Object_Number'))

Base.prepare(engine, reflect=True)
#session = Session(engine)

result = session.query(\
    Endocytosis.ImageNumber,\
    Endocytosis.Endocytosis_Parent_Cells,\
    func.sum(Endocytosis.Endocytosis_Intensity_IntegratedIntensity_Actin))\
    .group_by(Endocytosis.ImageNumber,Endocytosis.Endocytosis_Parent_Cells)

for r in result:
    print r

    #Endocytosis.Endocytosis_Number_Object_Number)\

    # .filter(Relationships.relationship_type_id == 1)\
    # .filter(Relationships.image_number1 == Cells.ImageNumber)\
    # .filter(Relationships.object_number1 == Cells.Cells_Number_Object_Number)\
    # .filter(Relationships.object_number2 == Endocytosis.Endocytosis_Number_Object_Number)

    # .filter(Endocytosis.Endocytosis_Parent_Cells == Relationships.object_number1)\
    # .filter(Endocytosis.ImageNumber == Relationships.image_number1)
    #.filter(Relationships.relationship_type_id == RelationshipTypes.relationship_type_id)
    #func.sum(Endocytosis.Endocytosis_Intensity_IntegratedIntensity_Actin))


# .filter(Endocytosis.Endocytosis_Parent_Cells == Relationships.object_number1)\
# .filter(Endocytosis.ImageNumber == Relationships.image_number1)\


#.filter(Cells.Cells_Number_Object_Number == Endocytosis.Endocytosis_Parent_Cells)\
#.all()
#.count()
