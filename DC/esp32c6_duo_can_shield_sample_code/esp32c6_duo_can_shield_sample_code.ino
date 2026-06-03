#include "driver/twai.h"

#define CAN_TX_GPIO  GPIO_NUM_5
#define CAN_RX_GPIO  GPIO_NUM_4

void setup() {
    Serial.begin(115200);
    delay(2000);

    twai_general_config_t g = TWAI_GENERAL_CONFIG_DEFAULT(
        CAN_TX_GPIO, CAN_RX_GPIO, TWAI_MODE_NORMAL
    );
    g.rx_queue_len = 32;
    g.tx_queue_len = 8;

    twai_timing_config_t t = TWAI_TIMING_CONFIG_500KBITS();
    twai_filter_config_t f = TWAI_FILTER_CONFIG_ACCEPT_ALL();

    twai_driver_install(&g, &t, &f);
    twai_start();
    Serial.println("CAN listo!");
}

void loop() {
    twai_status_info_t status;
    twai_get_status_info(&status);

    Serial.print("Estado: ");
    Serial.print(status.state);
    Serial.print(" | RX pending: ");
    Serial.print(status.msgs_to_rx);
    Serial.print(" | RX errors: ");
    Serial.print(status.rx_error_counter);
    Serial.print(" | TX errors: ");
    Serial.println(status.tx_error_counter);

    delay(1000);
}