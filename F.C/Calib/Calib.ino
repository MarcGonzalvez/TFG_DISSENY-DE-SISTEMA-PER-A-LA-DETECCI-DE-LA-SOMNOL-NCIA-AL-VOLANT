const int MIDA_ARRAY = 10000;
int captures[MIDA_ARRAY]; 
int comptador = 0; // Hem canviat 'index' per 'comptador'

void setup() {
  pinMode(34, INPUT);
  analogReadResolution(12);
  Serial.begin(115200);

}

void loop() {
  // Ara fem servir 'comptador'
  if (comptador < MIDA_ARRAY) {
    int valor = analogRead(34);

    // La teva rectificació
    /*if (valor <= 1900) {
     valor = 1900;
    }*/

    captures[comptador] = valor;
    comptador++;

    // Un delay de 2ms farà que capturis 1000 dades en uns 2 segons aprox.
    delay(2); 
  } 
  else if (comptador == MIDA_ARRAY) {
    
    for (int i = 0; i < MIDA_ARRAY; i++) {
      Serial.println(captures[i]);
    }

    comptador=0; // Sortim de la condició per no repetir el llistat infinitament

  }
}