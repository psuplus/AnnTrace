import os

for file_ in os.listdir(os.path.dirname(os.path.abspath(__file__))):
    fileext= os.path.splitext(file_)[1].replace(".","").lower()
    filename= os.path.splitext(file_)[0]
    if fileext == "py":
        __import__(f"examples.{filename}", globals(), locals())