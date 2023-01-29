char buffer[50];
char asdf;
void setup() {
  // put your setup code here, to run once:
Serial.begin(115200);
Serial1.begin(115200);
}

void loop() {
  if (Serial.available()){
    asdf = Serial.read();
    Serial1.print(asdf);
  }
}
