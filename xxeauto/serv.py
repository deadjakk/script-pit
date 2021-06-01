from flask import Flask
from flask import render_template
import sys

filenames=[]
i=0
app = Flask(__name__)

@app.route("/")
def kek():
    global i
    if i < len(filenames):
        filename = filenames[i]
        i+=1
        return render_template('thing.dtd', filename=filename)
    print ("out of filenames")
    sys.exit(0)

if __name__ == "__main__":
    with open ('filenames.txt','r') as fh:
        for line in fh.readlines():
            line=line.strip()
            filenames.append(line)
    print ('loaded {} filepaths'.format(len(filenames)))
    app.run(debug=True)
