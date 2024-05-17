
import datetime

from Control.DatabaseAdapter import DatabaseAdapter
from Model.tubeQrcode import TubeQrcode

def create_tube_qrcodes(value: int):
    # Überprüfen, ob der empfangene Wert ein Integer ist
    if isinstance(value, int):
        # Liste, um die erstellten TubeQrcode-Objekte zu speichern
        tube_qrcodes = []
        
        # Erstellen von TubeQrcode-Objekten in einer Schleife
        for i in range(value):
            qr_code = str(i + 1).zfill(6)  # QR-Code startet bei 000001
            datum = datetime.date.today()  # Aktuelles Datum
            tube_qrcode = TubeQrcode(qr_code, datum)
            tube_qrcodes.append(tube_qrcode)
        
        # Ausgabe der erstellten TubeQrcode-Objekte
        for tube_qrcode in tube_qrcodes:
            DatabaseAdapter.insert_data(tube_qrcode)
           # print(tube_qrcode)
    else:
        print("Der bereitgestellte Wert ist kein Integer.")


# create_tube_qrcodes(5)

