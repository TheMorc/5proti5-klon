//bez interruptov lebo som chuj a nekukol som si dopredu že iba piny 2 a 3 sú interruptové...
//nevadí, šak aj tak to moc nespraví rozdíl

int button1State = 0;
int button2State = 0;
int button1Lit = 0;
int button2Lit = 0;
int buttonReset = 0;
char serialChar = '.';

void setup() {
  Serial.begin(9600);
  pinMode(8, OUTPUT);
  pinMode(9, OUTPUT);
  
  pinMode(10, INPUT_PULLUP);
  pinMode(11, INPUT_PULLUP);
  
  Serial.println("5p5 setup done!");
}

void loop() {
  button1State = digitalRead(10);
  button2State = digitalRead(11);
  
  if (!button1State && !button2Lit && !button1Lit){
    button1Lit = 1;
    Serial.println("1");
    digitalWrite(8, 1);
  }

  if (!button2State && !button1Lit && !button2Lit){
    button2Lit = 1;
    Serial.println("2");
    digitalWrite(9, 1);
  }

  if (!button1State){
    Serial.println("1");
  }

  if (!button2State){
    Serial.println("2");
  }

  serialChar = Serial.read();
  if (serialChar == '0'){
    digitalWrite(8, 0);
    digitalWrite(9, 0);
    button1Lit = 0;
    button2Lit = 0;
  }
  else if (serialChar == '3'){
    digitalWrite(8, 1);
    digitalWrite(9, 1);
    delay(150);
    digitalWrite(8, 0);
    digitalWrite(9, 0);
    delay(150);
    digitalWrite(8, 1);
    digitalWrite(9, 1);
    delay(150);
    digitalWrite(8, 0);
    digitalWrite(9, 0);
    delay(150);
    digitalWrite(8, 1);
    digitalWrite(9, 1);
    delay(150);
    digitalWrite(8, 0);
    digitalWrite(9, 0);
    delay(150);
    digitalWrite(8, 1);
    digitalWrite(9, 1);
    delay(150);
    digitalWrite(8, 0);
    digitalWrite(9, 0);
    delay(150);
    digitalWrite(8, 1);
    digitalWrite(9, 1);
    delay(150);
    digitalWrite(8, 0);
    digitalWrite(9, 0);
    delay(150);
    digitalWrite(8, button1Lit);
    digitalWrite(9, button2Lit);
  }
}
