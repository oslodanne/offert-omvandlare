from flask import Flask, request, render_template
import re

app = Flask(__name__)

# Artikelregister med olika varianter av kundens benämning
artikelregister = {
    "6100fs nät": "DSM6100O",
    "6100# nät": "DSM6100O",
    "nätstöd 30mm": "DWS20A030",
    "speedies 30mm": "DPS02A030",
    "nätstöd 40mm": "DWS20A040",
    "5150#": "DSM5150SE",
    "8150 finger": "DSM8150O",
    "8150# finger": "DSM8150O",
    "6100# finger": "DSM6100O",
    "6150# finger": "DSM6150O",
    "10150# finger": "DSM10150O",
    "12150# finger": "DSM12150O",
    "6150#": "DSM6150SE",
    "6100#": "DSM6100O",
    "Kamstål 12mm x 6000mm": "WR671200600",
    "Kamstål 12mm": "WR671200600",
    "12mm 6000mm": "WR671200600",
    "Kamstål 16mm x 6000mm": "WR671600600",
    "12mm Kamstål": "WR671200600",
    "Kamstål 10mm x 6000mm": "WR671000600",
    "Linjal 25mm": "DPL01A025",
    "Linjal 30mm": "DPL01A030",
    "Distanslist 30mm": "DPL01A030",
    "Markdistans 40/50mm": "DPS01B040",
    "Speedies 40mm": "DPS02A040",
    "Nätstöd 90mm": "DWS20A090",
    "nätstöd 50mm": "DWS20A050",
    "Nätstöd 100mm": "DWS20A100",
    "Nätstöd 80mm": "DWS20A080",
    "Hullingar 180mm": "DBD01A180",
    "HULLINGAR 200mm": "DBD01A200",
    "Hullingar 100mm": "DBD01A100",
    "hulling 100mm": "DBD01A100",
    "Isoskruv 190mm": "DBD01B190",
    "Kantjärn 50x50x5x2500mm" :"DIA011001",
    "Kantjärn 50x50x5x3000mm": "DIA011002",
    "Kantjärn 50x50x5x4000mm" :"DIA011004",
    "Kantjärn 80x80x8x6000mm" :"DIA111004",
}

import re

def omvandla_text(text):
    resultat = []
    text = text.lower().strip()

    produkter = text.split("\n")

    for produkt in produkter:
        produkt = produkt.strip()
        
        if not produkt:  # Ignorera tomma rader
            continue  

        print(f"DEBUG - Ursprunglig rad: {produkt}")  

        produkt_rensad = re.sub(r'(\s+(st|m|mm|cm|g|kg))$', '', produkt)

        print(f"DEBUG - Rensad rad: {produkt_rensad}")  

        matchad = False

        for nyckel in sorted(artikelregister.keys(), key=len, reverse=True):
            if nyckel.lower() in produkt_rensad:
                resultat.append(artikelregister[nyckel])
                matchad = True
                break  

        if not matchad:
            resultat.append("Okänd")  

    return resultat if resultat else ["Inga matchningar hittades."]

def berakna_varde(input_text):
    resultat = []
    produktdata = {
        "86": {"artikel": "WR670800600", "vikt_st": 2.37, "vikt_m": 0.395, "langd_m": 6},
        "106": {"artikel": "WR671000600", "vikt_st": 3.71, "vikt_m": 0.617, "langd_m": 6},
        "126": {"artikel": "WR671200600", "vikt_st": 5.33, "vikt_m": 0.888, "langd_m": 6},
        "166": {"artikel": "WR671600600", "vikt_st": 9.48, "vikt_m": 1.58, "langd_m": 6},
        "206": {"artikel": "WR672000600", "vikt_st": 14.82, "vikt_m": 2.47, "langd_m": 6},
        "256": {"artikel": "WR672500600", "vikt_st": 23.1, "vikt_m": 3.85, "langd_m": 6},
        "6100fs": {"artikel": "DSM6100O", "tackande_yta": 11.76},
        "6150fs": {"artikel": "DSM6150O", "tackande_yta": 11.66},
        "7100fs": {"artikel": "DSM7100O", "tackande_yta": 11.00},
        "7150fs": {"artikel": "DSM7150O", "tackande_yta": 10.82},
        "8100fs": {"artikel": "DSM81000O", "tackande_yta": 11},
        "8150fs": {"artikel": "DSM8150O", "tackande_yta": 10.82},
        "9100fs": {"artikel": "DSM9100O", "tackande_yta": 10.26},
        "9150fs": {"artikel": "DSM9150O", "tackande_yta": 10.53},
        "10100fs": {"artikel": "DSM10100O", "tackande_yta": 10.26},
        "10150fs": {"artikel": "DSM10150O", "tackande_yta": 9.72},
        "102000fs": {"artikel": "DSM10200O", "tackande_yta": 9.72},
        "12100fs": {"artikel": "DSM12100O", "tackande_yta": 9.45},
        "12150fs": {"artikel": "DSM12150O", "tackande_yta": 9.45},
        "5150": {"artikel": "DSM5150SE", "tackande_yta": 9.70},
        "5200": {"artikel": "DSM5200SE", "tackande_yta": 9.10},
        "6150": {"artikel": "DSM6150SE", "tackande_yta": 9.70},
        "6200": {"artikel": "DSM6200SE", "tackande_yta": 9.10},
        "8150SE5": {"artikel": "DSM8150SE5", "tackande_yta": 9.40},
        "6100": {"artikel": "DSM6100SE", "tackande_yta": 11.58},
        "7150": {"artikel": "DSM7150SE", "tackande_yta": 11.58},
        "8150": {"artikel": "DSM8150SE", "tackande_yta": 11.47},
        "9150": {"artikel": "DSM9150SE", "tackande_yta": 11.16},
        "10150": {"artikel": "DSM10150SE", "tackande_yta": 10.86},
    }

    rader = input_text.lower().strip().split("\n")  # Dela upp inmatningen rad för rad

    for rad in rader:
        delar = rad.strip().split()

        if len(delar) < 2:
            resultat.append(("Fel", "Ange t.ex. '10st 86' eller '100m2 6150fs'"))
            continue

        antal, kod = delar[0], delar[1]

        if kod in produktdata:
            data = produktdata[kod]

            if "vikt_st" in data and "vikt_m" in data:  # Stångprodukter
                if "m" in antal:
                    meter = float(antal.replace("m", ""))
                    total_vikt = round(meter * data["vikt_m"], 2)
                else:
                    antal = int(antal.replace("st", ""))
                    total_vikt = round(antal * data["vikt_st"], 2)
                resultat.append((data["artikel"], f"{total_vikt}"))  # Endast siffror

            elif "tackande_yta" in data:  # Nätprodukter
                m2 = float(antal.replace("m2", ""))
                total_antal = round(m2 / data["tackande_yta"], 2)
                resultat.append((data["artikel"], f"{total_antal}"))  # Endast siffror

        else:
            resultat.append(("Okänd kod", kod))

    return resultat






@app.route('/', methods=['GET', 'POST'])
def index():
    artikelnummer = []
    kundtext = ""
    calculation_result = []
    calculation_input = ""  # Behåller texten i beräkningsfältet

    if request.method == 'POST':
        if 'kundtext' in request.form:
            kundtext = request.form['kundtext']
            artikelnummer = omvandla_text(kundtext)

        if 'calculation_input' in request.form:
            calculation_input = request.form['calculation_input']
            calculation_result = berakna_varde(calculation_input)

    return render_template('index.html', artikelnummer=artikelnummer, kundtext=kundtext, calculation_input=calculation_input, calculation_result=calculation_result)



import os
from flask import Flask



if __name__ == '__main__':  # Se till att detta har korrekt indragning
    port = int(os.environ.get("PORT", 10000))  # Render kräver en öppen port
    app.run(host="0.0.0.0", port=port)
