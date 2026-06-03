import serial
import csv

# Configura el port i la velocitat (revisa quin port COM fa servir el teu ESP32)
port_serie = 'COM6' 
baudrate = 115200
nom_fitxer = "dades_pulsacions2.csv"
mostres_totals = 10000

try:
    ser = serial.Serial(port_serie, baudrate, timeout=1)
    print(f"Connectat al port {port_serie}. Esperant dades...")

    dades_recollides = []
    comptador = 0

    while comptador < mostres_totals:
        linea = ser.readline().decode('utf-8').strip()
        
        if linea: # Si la línia no està buida
            try:
                valor = int(linea)
                dades_recollides.append(valor)
                comptador += 1
                if comptador % 100 == 0:
                    print(f"Capturades {comptador}/{mostres_totals} mostres...")
            except ValueError:
                # Per si arriba algun text de "Iniciant captura..." que no és un número
                continue

    # Guardar a un fitxer CSV
    with open(nom_fitxer, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(["Index", "Valor ADC"]) # Capçalera
        for i, v in enumerate(dades_recollides):
            writer.writerow([i, v])

    print(f"Fet! Dades guardades a '{nom_fitxer}'")
    ser.close()

except Exception as e:
    print(f"Error: {e}")