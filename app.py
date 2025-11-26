# Du musst Flask zuerst installieren: pip install Flask
from flask import Flask, request, jsonify
import json

# Erstellt die Web-Anwendung
app = Flask(__name__)

# Definiert den Endpunkt, den Bubble aufruft 
@app.route('/generate_zpl/', methods=['POST'])
def generate_zpl():
    try:
        # 1. Daten von Bubble empfangen
        data = request.json
        qr_code_id = data.get('qr_code_id')
        qr_target_url = data.get('qr_target_url') # Dies sollte die Basis-URL sein

        # 2. Logik: ZPL-Code generieren
        
        # Erzeuge den vollständigen Link für den QR-Code
        # WICHTIG: Verwende die von Bubble gesendete URL (qr_target_url) als Basis.
        qr_content = f"{qr_target_url}?qr_id={qr_code_id}"

        # **KRITISCHE LÖSUNG: PADDING**
        # Fügt 30 Leerzeichen hinzu, um die Datenmenge zu erhöhen
        # und den Drucker zur Wahl einer größeren, flächenfüllenden QR-Version zu zwingen.
        padding = "                                                                                                                                                      "  # 30 Leerzeichen
        qr_content_padded = qr_content + padding
        
        # ZPL-Code-Vorlage (203 DPI, 4x3 Zoll, 90 Grad Drehung)
        zpl_code = f"""
^XA
^LL609^PON                 
^PW812

^FW R

^FO50,50^BQN,2,8
^FDQA,{qr_content_padded}^FS

^FO600,50^A0R,50,50^FDZettelFix ID: {qr_code_id}^FS
^FO690,50^A0R,100,100^FDScan mich! :)^FS
^XZ
"""

        # 3. Antwort an Bubble zurücksenden
        response_data = {
            "status": "success",
            "zpl_code": zpl_code
        }
        return jsonify(response_data)

    except Exception as e:
        # Fehlerbehandlung
        return jsonify({"status": "error", "message": str(e)}), 400

# Startet den Server (für Tests)
if __name__ == '__main__':
    # Beispiel für den Aufruf der Funktion (lokale Tests)
    # print(generate_zpl({'qr_code_id': 'AB12345', 'qr_target_url': 'https://deineapp.bubbleapps.io/router'}))
    app.run(debug=True, port=5001)

