#define LED 13
#define OUT 3
#define MULTIPLIER 25

unsigned char message[100] = { 0 };
unsigned char counter = 0;

// Create the callback function
void processMessage() {
    int i = 0;
    int status = LOW;
    int out = 0;

    for (i = 0; i < counter; i++) {
        out = message[i] * MULTIPLIER;
        Serial.print(out);
        Serial.print(" ");
    }
    Serial.println("");

    for (i = 0; i < counter; i++) {
        if (status == HIGH) {
            status = LOW;
        } else {
            status = HIGH;
        }
        digitalWrite(OUT, status);
        out = message[i] * MULTIPLIER;
        delayMicroseconds(out);
    }
    digitalWrite(OUT, LOW);
}

void setup() {
    Serial.begin(9600);

    pinMode(LED, OUTPUT);
    pinMode(OUT, OUTPUT);
}

void loop() {
    unsigned char character = 0;

    while (Serial.available()) {
        if (counter >= 100) {
            counter = 0;
        }
        character = Serial.read();
        if (character == 0) {
            digitalWrite(LED, HIGH);
            processMessage();
            digitalWrite(LED, LOW);
            Serial.println("Command sent.");
            counter = 0;
        } else {
            message[counter] = character;
            counter++;
        }
    }

}
