
void setup() {
  // put your setup code here, to run once:
  Serial.begin(9600);
}

void loop() {
  // put your main code here, to run repeatedly:
  if (Serial.available()) {
    int x_mid, y_mid;
    if (Serial.read() == 'X') {
      x_mid = Serial.parseInt();  // read center x-coordinate
      if (Serial.read() == 'Y') {
        y_mid = Serial.parseInt(); // read center y-coordinate
      }
    }
    Serial.print("\t");
    Serial.print(x_mid);
    Serial.print("\t");
    Serial.println(y_mid);
  }
}
