from fireo.models import Model
from fireo.fields import *

class Hospitals(Model):
    name = TextField()

class Cases(Model):
    status = TextField()
    test = TextField()
    hospitals = NestedModel(Hospitals)

class hospital_details(Model):
    name = TextField()
    Date_of_Admission = TextField()
    cases = NestedModel(Cases)

class patient_details(Model):
    Name = TextField()
    Insurance_Company = TextField()
    cases = NestedModel(Cases)