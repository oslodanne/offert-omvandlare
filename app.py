from flask import Flask, request, render_template
import re

app = Flask(__name__)

# Artikelregister med olika varianter av kundens benämning
artikelregister = {
    "6100fs nät": "dsm6100o",
    "6100# nät": "dsm6100o",
    "nätstöd 30mm": "dws20a030",
    "speedies 40mm": "dps02a040",
    "speedies 30mm": "dps02a030"
}

def omvandla_text(text):
    resultat = []
    text = text.lower()
    
    hittade_produkter = set()
    for produkt, artikelnummer in artikelregister.items():
        if re.search(rf'\b{re.escape(produkt)}\b', text):
            resultat.append(artikelnummer)
            hittade_produkter.add(produkt)
    
    # Hitta ord som inte matchar något i artikelregistret
    ord_lista = text.split()
    for ordet in ord_lista:
        if not any(re.search(rf'\b{re.escape(produkt)}\b', ordet) for produkt in artikelregister.keys()):
            resultat.append("Okänd")
    
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

