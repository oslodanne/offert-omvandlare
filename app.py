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
    
    for produkt, artikelnummer in artikelregister.items():
        if re.search(rf'\b{re.escape(produkt)}\b', text):
            resultat.append(artikelnummer)
    
    if not resultat:
        return "Inga matchningar hittades."
    
    return ', '.join(resultat)

@app.route('/', methods=['GET', 'POST'])
def index():
    artikelnummer = ""
    if request.method == 'POST':
        kundtext = request.form['kundtext']
        artikelnummer = omvandla_text(kundtext)
    return render_template('index.html', artikelnummer=artikelnummer)

if __name__ == '__main__':
    app.run(debug=True)

