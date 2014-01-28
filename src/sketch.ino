#define LED 13
#define TIMING_MULTIPLIER 25
#define DELAY_MULTIPLIER 100
#define MAX_MESSAGE_LENGTH 100

unsigned char gMessage[MAX_MESSAGE_LENGTH] = { 0 };
unsigned char gCounter = 0;

void transmit(char pin, unsigned char message[], unsigned char repeat, unsigned int intraDelay) {
    int status = LOW;
    unsigned int out = 0;
    unsigned char i, j;

    pinMode(pin, OUTPUT);

    // Send the message.
    for (j = 0; j < repeat; j++) {
        for (i = 0; i < MAX_MESSAGE_LENGTH; i++) {
            if (message[i] == 0) break;

            if (status == HIGH) {
                status = LOW;
            } else {
                status = HIGH;
            }
            digitalWrite(pin, status);
            out = message[i] * TIMING_MULTIPLIER;
            delayMicroseconds(out);
        }

        // Reset, just in case.
        digitalWrite(pin, LOW);
        delayMicroseconds(intraDelay);
    }
}

// Create the callback function
void cmdSend(char pin, unsigned char message[], unsigned char repeat, unsigned int intraDelay) {
    unsigned int out = 0;
    unsigned char i;

    digitalWrite(LED, HIGH);

    Serial.print("Sending on pin ");
    Serial.print(pin, DEC);
    Serial.print(", repeating ");
    Serial.print(repeat, DEC);
    Serial.print(" times, for ");
    Serial.print(intraDelay);
    Serial.println(" microseconds.");

    // Print the received timings to the console.
    for (i = 0; i < MAX_MESSAGE_LENGTH; i++) {
        if (message[i] == 0) break;
        out = message[i] * TIMING_MULTIPLIER;
        Serial.print(out);
        Serial.print(" ");
    }
    Serial.print("\r\n");

    transmit(pin, message, repeat, intraDelay);

    digitalWrite(LED, LOW);
    Serial.println("Command sent.");
}

void setup() {
    Serial.begin(9600);

    pinMode(LED, OUTPUT);
}

void loop() {
    unsigned char character = 0;

    while (Serial.available()) {
        if (gCounter >= MAX_MESSAGE_LENGTH) gCounter = 0;

        character = Serial.read();
        gMessage[gCounter++] = character;

        // Process the message if we receive a null.
        if (character != 0) continue;

        // Don't process early if the command is 1, because pin may also be a 0.
        if ((gMessage[0] == 1) && (gCounter < 3)) continue;

        switch (gMessage[0]) {
            case 1:
                cmdSend(gMessage[1], &gMessage[4], gMessage[2], gMessage[3] * DELAY_MULTIPLIER);
                break;
        }

        gCounter = 0;
    }
}
