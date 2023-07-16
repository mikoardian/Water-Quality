# =[Modules dan Packages]========================

from flask import Flask,render_template,request,jsonify
import pandas as pd
from joblib import load
import os

# =[Variabel Global]=============================

app   = Flask(__name__, static_url_path='/static')
#model = None

# =[Routing]=====================================

# [Routing untuk Halaman Utama atau Home]	
@app.route("/")
def beranda():
    return render_template('index.html')

# [Routing untuk API]    
@app.route("/api/deteksi", methods=['POST'])
def apiDeteksi():
    # Nilai default untuk variabel input atau features (X) ke model
    input_cadmium = 0.5
    input_aluminium = 3
    input_perchlorate = 30
    input_ammonia = 10
    input_uranium = 0.04
    input_silver= 0.25
    input_nitrates = 9
    input_radium = 3.5
    input_nitrites = 1
    input_bacteria = 0.5
    input_viruses = 0.5
    input_chloramine = 4

    if request.method == 'POST':
        # Set nilai untuk variabel input atau features (X) berdasarkan input dari pengguna
        input_cadmium       = float(request.form['cadmium'])
        input_aluminium     = float(request.form['aluminium'])
        input_perchlorate   = float(request.form['perchlorate'])
        input_ammonia       = float(request.form['ammonia'])
        input_uranium       = float(request.form['uranium'])
        input_silver        = float(request.form['silver'])
        input_nitrates      = float(request.form['nitrates'])
        input_radium        = float(request.form['radium'])
        input_nitrites      = float(request.form['nitrites'])
        input_bacteria      = float(request.form['bacteria'])
        input_viruses       = float(request.form['viruses'])
        input_chloramine    = float(request.form['chloramine'])

        # Prediksi kelas
        df_test = pd.DataFrame(data={
            "cadmium"       : [input_cadmium],
            "aluminium"     : [input_aluminium],
            "perchlorate"   : [input_perchlorate],
            "ammonia"       : [input_ammonia],
            "uranium"       : [input_uranium],
            "silver"        : [input_silver],
            "nitrates"      : [input_nitrates],
            "radium"        : [input_radium],
            "nitrites"      : [input_nitrites],
            "bacteria"      : [input_bacteria],
            "viruses"       : [input_viruses],
            "chloramine"    : [input_chloramine],
        })

        hasil_prediksi = model.predict(df_test[0:1])[0]

        # Set Path untuk gambar hasil prediksi
        if hasil_prediksi == 0:
            hasil_prediksi_label = "Air Layak Konsumsi"
            gambar_prediksi = '/static/images/airkonsumsi.png'
        else:
            hasil_prediksi_label = "Air Tidak Layak Konsumsi"
            gambar_prediksi = '/static/images/airtidakkonsumsi.png'

        # Return hasil prediksi dengan format JSON
        return jsonify({
            "prediksi": hasil_prediksi_label,
            "gambar_prediksi": gambar_prediksi
        })

# =[Main]========================================

if __name__ == '__main__':
	
	# Load model yang telah ditraining
	model = load('model_wq_dt.model')

	# Run Flask di localhost 
	app.run(host="0.0.0.0", port=int(os.environ.get('PORT', 8080)))