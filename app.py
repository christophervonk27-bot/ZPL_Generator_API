# Du musst Flask zuerst installieren: pip install Flask
from flask import Flask, request, jsonify
import json

# Erstellt die Web-Anwendung
app = Flask(__name__)

# Definiert den Endpunkt, den Bubble aufruft 
# (z.B. https://api.dein-service.com/generate_zpl/)
@app.route('/generate_zpl/', methods=['POST'])
def generate_zpl():
    try:
        # 1. Daten von Bubble empfangen
        data = request.json
        qr_code_id = data.get('qr_code_id')
        qr_target_url = data.get('qr_target_url')

        # 2. Logik: ZPL-Code generieren
        #    Wir bauen den Text-String für den ZPL-Drucker
        
        # Erzeuge den Link für den QR-Code (ERSETZE 'DEINE-APP' HIER!)
        qr_content = f"https://christophervonk27.bubbleapps.io/router?qr_id={qr_code_id}"

        # ZPL-Code-Vorlage
        # ^BQN... ist der Befehl für einen QR-Code
        zpl_code = f"""
^XA
^FO50,50^A0N,30,30^FDQR-ID: {qr_code_id}^FS
^FO50,100^BQN,2,8^FDQA,{qr_content}^FS
^FO50,350^A0N,25,25^FDScan fuer Details^FS
^XZ
"""

        # 3. Antwort an Bubble zurücksenden
        #    Genau das JSON-Format, das wir im API Connector initialisiert haben
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
    app.run(debug=True, port=5001)