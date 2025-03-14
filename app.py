from flask import Flask, request, render_template
import re

app = Flask(__name__)

# Artikelregister med olika varianter av kundens benämning
artikelregister = {
    "6100fs nät": "DSM6100O",
    "6100# nät": "DSM6100O",
    "nätstöd 30mm": "DWS20A030",
    "speedies 40mm": "DWS20A040",
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
    "hullingar": "DBD01A180",
    "Hullingar 180mm": "DBD01A180",
    "Hullingar 100mm": "DBD01A100",
    "hulling 100mm": "DBD01A100",
    "Isoskruv 190mm": "DBD01B190",
    "Kantjärn 50x50x5x2500mm" :"DIA011001",
    "Kantjärn 50x50x5x3000mm": "DIA011002",
    "Kantjärn 50x50x5x4000mm" :"DIA011004",
    "Kantjärn 80x80x8x6000mm" :"DIA111004",
}

def omvandla_text(text):
    resultat = []
    text = text.lower().strip()
    
    # Dela upp texten i rader eller delar baserat på radbrytningar och komma
    produkter = re.split(r'[\n,]+', text)

    for produkt in produkter:
        produkt = produkt.strip()  # Ta bort mellanslag runt produkten
        matchad = False

        # Sortera artikelregister-nycklarna efter längd för att hitta den längsta möjliga matchen först
        for nyckel in sorted(artikelregister.keys(), key=len, reverse=True):
            if re.search(re.escape(nyckel.lower()), produkt):  
                resultat.append(artikelregister[nyckel])
                matchad = True
                break  # Avsluta loopen så fort vi hittar en match

        if not matchad:
            resultat.append("Okänd")  # Lägg endast till en "Okänd" per produkt

    return resultat if resultat else ["Inga matchningar hittades."]




@app.route('/', methods=['GET', 'POST'])
def index():
    artikelnummer = []
    kundtext = ""
    if request.method == 'POST':
        kundtext = request.form['kundtext']
        artikelnummer = omvandla_text(kundtext)
    return render_template('index.html', artikelnummer=artikelnummer, kundtext=kundtext)

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 10000))  # Standardport 5000 om PORT inte sätts
    app.run(host='0.0.0.0', port=port, debug=True)

