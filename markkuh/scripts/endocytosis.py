import sqlalchemy
from sqlalchemy import create_engine

#dbpath = "sqlite:////home/hajaalin/tmp/mkhakala/EndocytosisTWF1+2-KO.db"
dbpath = "sqlite:////vagrant/data/EndocytosisTWF1+2-KO.db"
print dbpath

engine = create_engine(dbpath)
conn = engine.connect()

from sqlalchemy import MetaData
m = MetaData()
m.reflect(engine)
for table in m.tables.values():
    print("TABLE " + table.name)
    for column in table.c:
        print(column.name)
    print

from sqlalchemy.ext.automap import automap_base
#from sqlalchemy.orm import Session
import sqlalchemy.orm
from sqlalchemy.orm import sessionmaker
from sqlalchemy import func

Session = sessionmaker(bind=engine)
session = Session()

Base = automap_base()
Base.prepare(engine, reflect=True)

Image = Base.classes.TWFKO_Per_Image
Endocytosis = Base.classes.TWFKO_Per_Endocytosis
Cells = Base.classes.TWFKO_Per_Cells
RelationshipTypes = Base.classes.TWFKO_Per_RelationshipTypes
Relationships = Base.classes.TWFKO_Per_Relationships
#sqlalchemy.orm.join(Cells, Endocytosis, onclause=Cells.Cells_Number_Object_Number == Endocytosis.Endocytosis_Parent_Cells)


#print session.query(Image.ImageNumber,Cells.Cells_Number_Object_Number,func.sum(Endocytosis.Endocytosis_Intensity_IntegratedIntensity_Actin))\
#.filter(Cells.ImageNumber == Image.ImageNumber)\
#.filter(Endocytosis.ImageNumber == Image.ImageNumber)\
#.filter(RelationshipTypes.relationship == "Parent")\
#.filter(RelationshipTypes.relationship_type_id == Relationships.relationship_type_id)\
#.filter(Endocytosis.Endocytosis_Parent_Cells == Relationships

print session.query(Relationships.image_number1,Relationships.object_number1,func.sum(Endocytosis.Endocytosis_Intensity_IntegratedIntensity_Actin))\
.filter(Endocytosis.Endocytosis_Parent_Cells == Relationships.object_number1)\
.all()


#.filter(Cells.Cells_Number_Object_Number == Endocytosis.Endocytosis_Parent_Cells)\
#.all()
#.count()


