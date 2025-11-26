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
        qr_target_url = data.get('qr_target_url') 

        # 2. Logik: ZPL-Code generieren
        
        # **KRITISCHE KORREKTUR:** Wir verwenden die vollständige URL, die von Bubble gesendet wurde.
        # Wir fügen KEINE weiteren '?qr_id=' Parameter hinzu, da Bubble dies bereits tut.
        qr_content = qr_target_url 

        # **LÖSUNG: PADDING**
        # Fügt 30 Leerzeichen hinzu, um die Datenmenge zu erhöhen
        # und den Drucker zur Wahl einer größeren, flächenfüllenden QR-Version zu zwingen.
        padding = "                              "  # 30 Leerzeichen
        qr_content_padded = qr_content + padding
        
        # ZPL-Code-Vorlage (203 DPI, 4x3 Zoll, 90 Grad Drehung)
        zpl_code = f"""
^XA
^LL609^PON                 
^PW812                     <-- Fixiert die Breite auf 4 Zoll / 812 Punkte (203 DPI)

^FW R                      <-- 90 Grad Drehung

^FO50,50^BQN,2,17          <-- Modulgröße 17 (optimal für 4-Zoll-Drucker)
^FDQA,{qr_content_padded}^FS

^FO550,50^A0R,50,50^FDZettelFix ID: {qr_code_id}^FS <-- Korrigierte X-Koordinate für 90-Grad-Drehung
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
    app.run(debug=True, port=5001)
