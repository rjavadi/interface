from flask import Flask, render_template, request
import pandas as pd 
import csv
from collections import defaultdict
import random
app = Flask(__name__, static_folder='./static')

@app.route('/',methods = ["GET","POST"])
def initial():
    return render_template('main.html')

@app.route('/home',methods = ["GET","POST"])
def home():
    if request.method == "POST":
         return render_template('home.html')
    return render_template('home.html')


@app.route('/index', methods = ["GET", "POST"]) 
def index():
    d = None
    if request.method == "POST":
        #print(request.form)
        j = request.form
        k = request.form.getlist('culture')
        
        #if statement is for setting up the csv file 
        #Write each parameter to a txt file so it can be called later and stored in csv file. 

        if len(k) > 0:
            
            cult = j['culture']
            IDV = j['IDV']
            nat = j['country']
            lang = j['language']
            with open("store_culture.txt", "a+") as file_object:
                file_object.seek(0)
                data = file_object.read(100)
                if len(data) > 0:
                    file_object.write("\n")
                file_object.write(nat)
                file_object.write("\n")
                file_object.write(lang)
                file_object.write("\n")
                file_object.write(cult)
                file_object.write("\n")
                file_object.write(IDV)

            vid = 'video' + str(random.randint(1,6)) + '.mp4'
            with open("store_video.txt", "a+") as file_object:
                file_object.seek(0)
                data = file_object.read(100)
                if len(data) > 0:
                    file_object.write("\n")
                file_object.write(vid)

            return render_template('index.html', video = vid)

        #this component takes user input after initial setup
        d = request.form.to_dict() 
        r = open("store_culture.txt", "r") #read last 4 items stored from the txt file from initial setup 
        #print(r)
        word = r.read().splitlines()
        #print(word)
        p = word[-1]
        s = word[-2]
        q = word[-3]
        t = word[-4]
        d['culture'] = p
        d['language'] = s
        d['country'] = q
        d['IDV'] = t
        
        
        r = open("store_video.txt", "r")
        n = r.readline()
        word = n.split()
        v = word[-1]
        d['video'] = v

        grp = defaultdict(list)
        for k, v in d.items():
            if k[0:3] == "soc":
                grp['socialsignals'].append(v)
            else:
                grp[k] = v
        print(grp)


        fields = grp.values()
        #print(fields)
        
        #writes everything that is in the dictionary to the csv file
        with open('out.csv', 'a+', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(fields)
        
        #store new video so it can be used for the next setup of user input
        vid = 'video' + str(random.randint(1,6)) + '.mp4'
        with open("store_video.txt", "a+") as file_object:
                file_object.seek(0)
                data = file_object.read(100)
                if len(data) > 0:
                    file_object.write("\n")
                file_object.write(vid)
        return render_template('index.html', video = vid)
  
    vid = 'video' + str(random.randint(1,6)) + '.mp4'
    return render_template('index.html', video = vid)



if __name__ == '__main__':
	app.debug = True
	app.run(host = '0.0.0.0', port = 5000)