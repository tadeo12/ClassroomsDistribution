import json
from Models.Commission import *
from Models.Teacher import *
from Models.Subject import *

teacher = Teacher("juan")
subject = Subject("matematica")

comision = Commission("comision1",teacher, subject, 20)

print(id(comision))