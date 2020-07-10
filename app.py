from flask import Flask,jsonify,request, render_template,flash,redirect,url_for,abort,session
from flask_apscheduler import APScheduler
from view.db import dblite as db
from view.db import sqlComment as sq
import requests as rq,atexit
from datetime import datetime

app = Flask(__name__, static_url_path='/static')
app.config.from_object(__name__)
app.config['SECRET_KEY'] = '1ace0c64-f122-52bb-b370-9830f91fb9b1'

port = 8000

def my_job():
    sensor_type = []
    value = []
    date_now = datetime.now().strftime('%d/%m/%Y')
    time_now = datetime.now().strftime('%H:%M:%S')
    SelectTree = db.select_json(sq.SelectTree)
    IdTree = []
    for i in SelectTree:
        IdTree.append(i["id"])
    for i in IdTree:
        value.append(i)
        for x in range(10):
            url = "https://belajar-python-unsyiah.an.r.appspot.com/sensor/read?npm=1904111010018&id_tree="+str(i)+"&sensor_type="+str(x)
            r = rq.get(url=url)
            data = r.json()
            sensor_type.append(data["sensor_type"])
            value.append(data["value"])
        value.append(date_now)
        value.append(time_now)
        db.cud(sq.InsertSensor,value)
        print("Succes to crawling data for id :"+str(i)+" pada waktu :"+time_now)
        value = []


@app.route('/', methods=['GET','POST'])
def home():
    if request.method == 'GET':
        tree = db.select_json(sq.SelectTree)
        return render_template('section/home/home.html',tree=tree)
    else:
        name = request.form['nama']
        _db_coordinate = db.select_json(sq.SelectCoordinate)
        coordinates = []
        for x in range(5):
            for y in range(5):
                coordinates.append((x, y))
        if not _db_coordinate:
            valInsert = (name,str(coordinates[0]),)
            db.cud(sq.InsertTree,valInsert)
        else:
            index_coor = db.select_json(sq.SelectIndexCoordinate)[0]['posisi']
            print(index_coor)
            if index_coor <= len(coordinates):
                valInsert = [name,str(coordinates[index_coor+1]),index_coor+1]
                print(valInsert)
                # db.cud(sq.InsertTree,valInsert)
                flash('Scs','Success adding new tree')
                return redirect(url_for('home'))
            else:
                flash('Err','Sorry the field has been fulled, please delete tree first')
                return redirect(url_for('home'))

@app.route('/delete', methods=['POST'])
def delete():
    id = request.args.get('id')
    db.cud(sq.DeleteTree,(id,))
    flash('Scs','Success to delete tree')
    return redirect(url_for('home'))
    
@app.route('/detail', methods=['GET'])
def detail():
    id = request.args.get('id')
    name = request.args.get('name')
    date_now = datetime.now().strftime('%d/%m/%Y')
    valSelect = (id,date_now,)
    data = db.selectId_json(sq.SelectSensorById,valSelect)
    suhu_udara = []
    kelembaban_udara = []
    curah_hujan = []
    uv = []
    suhu_tanah = []
    kelembaban_tanah = []
    ph = []
    kadar_n = []
    kadar_p = []
    kadar_k = []
    time = []
    for i in data:
        suhu_udara.append(i["suhu_udara"])
        kelembaban_udara.append(i["kelembaban_udara"])
        curah_hujan.append(i["curah_hujan"])
        uv.append(i["uv"])
        suhu_tanah.append(i["suhu_tanah"])
        kelembaban_tanah.append(i["kelembaban_tanah"])
        ph.append(i["ph"])
        kadar_n.append(i["kadar_n"])
        kadar_p.append(i["kadar_p"])
        kadar_k.append(i["kadar_k"])
        time.append(i["time"])
    return render_template('section/home/detail.html',name=name,date_now=date_now, suhu_udara=suhu_udara,kelembaban_udara=kelembaban_udara,curah_hujan=curah_hujan,uv=uv,suhu_tanah=suhu_tanah,kelembaban_tanah=kelembaban_tanah,ph=ph,kadar_n=kadar_n,kadar_p=kadar_p,kadar_k=kadar_k,time=time)

@app.route('/average', methods=['GET'])
def average():
    date_now = datetime.now().strftime('%d/%m/%Y')
    data = db.selectId_json(sq.AverageSensor,(date_now,))
    date_db = db.select_json(sq.SelectDistinct)
    suhu_udara = []
    kelembaban_udara = []
    curah_hujan = []
    uv = []
    suhu_tanah = []
    kelembaban_tanah = []
    ph = []
    kadar_n = []
    kadar_p = []
    kadar_k = []
    date_all = []
    for i in date_db:
        data = db.selectId_json(sq.AverageSensor,(i["date"],))
        for x in data:
            suhu_udara.append(x["avg_suhu_udara"])
            kelembaban_udara.append(x["avg_kelembaban_udara"])
            curah_hujan.append(x["avg_curah_hujan"])
            uv.append(x["avg_uv"])
            suhu_tanah.append(x["avg_suhu_tanah"])
            kelembaban_tanah.append(x["avg_kelembaban_tanah"])
            ph.append(x["avg_ph"])
            kadar_n.append(x["avg_kadar_n"])
            kadar_p.append(x["avg_kadar_p"])
            kadar_k.append(x["avg_kadar_k"])
        date_all.append(i["date"])

    return render_template('section/home/detail.html',suhu_udara=suhu_udara,kelembaban_udara=kelembaban_udara,curah_hujan=curah_hujan,uv=uv,suhu_tanah=suhu_tanah,kelembaban_tanah=kelembaban_tanah,ph=ph,kadar_n=kadar_n,kadar_p=kadar_p,kadar_k=kadar_k,time=date_all)

if __name__ == '__main__':
    scheduler = APScheduler()
    scheduler.add_job(func=my_job, trigger='interval', id='job', minutes=1)
    scheduler.start()
    app.run(debug=False, port=port, host='0.0.0.0')
