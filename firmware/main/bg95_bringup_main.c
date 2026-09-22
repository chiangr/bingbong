/*
 * BG95 bring-up step 1: enable the board's 1.8 V logic rail.
 */

#include <stdbool.h>
#include <stddef.h>
#include <stdint.h>
#include <string.h>

#include "driver/gpio.h"
#include "driver/uart.h"
#include "esp_check.h"
#include "esp_err.h"
#include "esp_log.h"
#include "freertos/FreeRTOS.h"
#include "freertos/task.h"

#define BG95_1V8_EN_GPIO GPIO_NUM_13
#define BG95_PWRKEY_GPIO GPIO_NUM_12
#define BG95_SIM_SW_GPIO GPIO_NUM_33
#define BG95_UART_TX_GPIO GPIO_NUM_1
#define BG95_UART_RX_GPIO GPIO_NUM_2

#define BG95_UART_PORT UART_NUM_1
#define BG95_UART_BAUD 115200
#define BG95_UART_RX_BUF_SIZE 2048
#define BG95_UART_TX_BUF_SIZE 256

#define BG95_1V8_ENABLE_LEVEL 1
#define BG95_1V8_DISABLE_LEVEL 0

/*
 * GPIO12 drives Q1 through R1. High on this net pulls BG95 PWRKEY low.
 * Keep it low for this first rail-only test.
 */
#define BG95_PWRKEY_RELEASE_LEVEL 0
#define BG95_PWRKEY_ASSERT_LEVEL 1

#define BG95_RAIL_SETTLE_MS 250
#define BG95_PWRKEY_PULSE_MS 800
#define BG95_BOOT_WAIT_MS 8000
#define BG95_AT_RESPONSE_TIMEOUT_MS 2500
#define BG95_STATUS_LOG_MS 1000
#define BG95_AT_KEEPALIVE_MS 10000

static const char *TAG = "bg95_bringup";
static int s_1v8_enable_commanded = BG95_1V8_DISABLE_LEVEL;
static int s_pwrkey_commanded = BG95_PWRKEY_RELEASE_LEVEL;

static esp_err_t bg95_gpio_init(void)
{
    gpio_config_t output_config = {
        .pin_bit_mask = (1ULL << BG95_1V8_EN_GPIO) |
                        (1ULL << BG95_PWRKEY_GPIO),
        .mode = GPIO_MODE_INPUT_OUTPUT,
        .pull_up_en = GPIO_PULLUP_DISABLE,
        .pull_down_en = GPIO_PULLDOWN_DISABLE,
        .intr_type = GPIO_INTR_DISABLE,
    };
    ESP_RETURN_ON_ERROR(gpio_config(&output_config), TAG, "GPIO output config failed");

    gpio_config_t input_config = {
        .pin_bit_mask = (1ULL << BG95_SIM_SW_GPIO),
        .mode = GPIO_MODE_INPUT,
        .pull_up_en = GPIO_PULLUP_ENABLE,
        .pull_down_en = GPIO_PULLDOWN_DISABLE,
        .intr_type = GPIO_INTR_DISABLE,
    };
    ESP_RETURN_ON_ERROR(gpio_config(&input_config), TAG, "GPIO input config failed");

    ESP_RETURN_ON_ERROR(gpio_set_level(BG95_PWRKEY_GPIO, BG95_PWRKEY_RELEASE_LEVEL),
                        TAG, "failed to release BG95 PWRKEY");
    s_pwrkey_commanded = BG95_PWRKEY_RELEASE_LEVEL;
    ESP_RETURN_ON_ERROR(gpio_set_level(BG95_1V8_EN_GPIO, BG95_1V8_DISABLE_LEVEL),
                        TAG, "failed to disable BG95 1.8 V rail");
    s_1v8_enable_commanded = BG95_1V8_DISABLE_LEVEL;

    return ESP_OK;
}

static esp_err_t bg95_uart_init(void)
{
    const uart_config_t uart_config = {
        .baud_rate = BG95_UART_BAUD,
        .data_bits = UART_DATA_8_BITS,
        .parity = UART_PARITY_DISABLE,
        .stop_bits = UART_STOP_BITS_1,
        .flow_ctrl = UART_HW_FLOWCTRL_DISABLE,
        .source_clk = UART_SCLK_DEFAULT,
    };

    ESP_RETURN_ON_ERROR(uart_driver_install(BG95_UART_PORT,
                                            BG95_UART_RX_BUF_SIZE,
                                            BG95_UART_TX_BUF_SIZE,
                                            0,
                                            NULL,
                                            0),
                        TAG, "UART driver install failed");
    ESP_RETURN_ON_ERROR(uart_param_config(BG95_UART_PORT, &uart_config),
                        TAG, "UART parameter config failed");
    ESP_RETURN_ON_ERROR(uart_set_pin(BG95_UART_PORT,
                                     BG95_UART_TX_GPIO,
                                     BG95_UART_RX_GPIO,
                                     UART_PIN_NO_CHANGE,
                                     UART_PIN_NO_CHANGE),
                        TAG, "UART pin config failed");

    ESP_LOGI(TAG, "BG95 UART%d ready: TX GPIO%d -> BG95 MAIN_RXD, RX GPIO%d <- BG95 MAIN_TXD, %d baud",
             BG95_UART_PORT, BG95_UART_TX_GPIO, BG95_UART_RX_GPIO, BG95_UART_BAUD);
    return ESP_OK;
}

static void bg95_enable_1v8_rail(void)
{
    ESP_LOGI(TAG, "Holding BG95 PWRKEY inactive on GPIO%d", BG95_PWRKEY_GPIO);
    ESP_LOGI(TAG, "Enabling BG95 1.8 V rail: GPIO%d -> %d",
             BG95_1V8_EN_GPIO, BG95_1V8_ENABLE_LEVEL);
    ESP_ERROR_CHECK(gpio_set_level(BG95_1V8_EN_GPIO, BG95_1V8_ENABLE_LEVEL));
    s_1v8_enable_commanded = BG95_1V8_ENABLE_LEVEL;
    vTaskDelay(pdMS_TO_TICKS(BG95_RAIL_SETTLE_MS));
}

static void bg95_pulse_pwrkey(void)
{
    ESP_LOGI(TAG, "Pulsing BG95 PWRKEY for %d ms", BG95_PWRKEY_PULSE_MS);
    ESP_ERROR_CHECK(gpio_set_level(BG95_PWRKEY_GPIO, BG95_PWRKEY_ASSERT_LEVEL));
    s_pwrkey_commanded = BG95_PWRKEY_ASSERT_LEVEL;
    vTaskDelay(pdMS_TO_TICKS(BG95_PWRKEY_PULSE_MS));

    ESP_ERROR_CHECK(gpio_set_level(BG95_PWRKEY_GPIO, BG95_PWRKEY_RELEASE_LEVEL));
    s_pwrkey_commanded = BG95_PWRKEY_RELEASE_LEVEL;
    ESP_LOGI(TAG, "Released BG95 PWRKEY; waiting %d ms for modem boot", BG95_BOOT_WAIT_MS);
    vTaskDelay(pdMS_TO_TICKS(BG95_BOOT_WAIT_MS));
}

static esp_err_t bg95_send_at_command(const char *command, char *response, size_t response_size)
{
    if (response_size == 0) {
        return ESP_ERR_INVALID_ARG;
    }

    response[0] = '\0';
    ESP_ERROR_CHECK(uart_flush_input(BG95_UART_PORT));

    ESP_LOGI(TAG, "BG95 << %s", command);
    ESP_RETURN_ON_FALSE(uart_write_bytes(BG95_UART_PORT, command, strlen(command)) == (int)strlen(command),
                        ESP_FAIL, TAG, "UART command write failed");
    ESP_RETURN_ON_FALSE(uart_write_bytes(BG95_UART_PORT, "\r\n", 2) == 2,
                        ESP_FAIL, TAG, "UART line ending write failed");

    const int64_t deadline_ticks = xTaskGetTickCount() + pdMS_TO_TICKS(BG95_AT_RESPONSE_TIMEOUT_MS);
    size_t response_len = 0;

    while (xTaskGetTickCount() < deadline_ticks && response_len < response_size - 1) {
        uint8_t byte = 0;
        const int read_len = uart_read_bytes(BG95_UART_PORT, &byte, 1, pdMS_TO_TICKS(50));
        if (read_len > 0) {
            response[response_len++] = (char)byte;
            response[response_len] = '\0';

            if (strstr(response, "\r\nOK\r\n") != NULL ||
                strstr(response, "\r\nERROR\r\n") != NULL ||
                strstr(response, "\r\n+CME ERROR:") != NULL) {
                break;
            }
        }
    }

    if (response_len == 0) {
        ESP_LOGW(TAG, "BG95 >> no response within %d ms", BG95_AT_RESPONSE_TIMEOUT_MS);
        return ESP_ERR_TIMEOUT;
    }

    ESP_LOGI(TAG, "BG95 >> %s", response);
    return ESP_OK;
}

static bool bg95_probe_at(int attempts)
{
    char response[128];

    for (int attempt = 1; attempt <= attempts; attempt++) {
        const esp_err_t ret = bg95_send_at_command("AT", response, sizeof(response));
        if (ret == ESP_OK && strstr(response, "OK") != NULL) {
            ESP_LOGI(TAG, "BG95 AT probe passed on attempt %d", attempt);
            return true;
        }

        ESP_LOGW(TAG, "BG95 AT probe attempt %d/%d failed", attempt, attempts);
        vTaskDelay(pdMS_TO_TICKS(1000));
    }

    return false;
}

static bool bg95_run_at_smoke_test(void)
{
    char response[512];
    const char *commands[] = {
        "AT",
        "ATE0",
        "ATI",
        "AT+CPIN?",
        "AT+QCCID",
        "AT+CSQ",
    };

    ESP_LOGI(TAG, "Starting BG95 AT smoke test");
    for (size_t i = 0; i < sizeof(commands) / sizeof(commands[0]); i++) {
        const esp_err_t ret = bg95_send_at_command(commands[i], response, sizeof(response));
        if (ret != ESP_OK) {
            ESP_LOGW(TAG, "Stopping AT smoke test at '%s': %s",
                     commands[i], esp_err_to_name(ret));
            return false;
        }
        vTaskDelay(pdMS_TO_TICKS(250));
    }
    ESP_LOGI(TAG, "BG95 AT smoke test complete");
    return true;
}

void app_main(void)
{
    ESP_LOGI(TAG, "Starting BG95 power-on and AT bring-up test");
    ESP_ERROR_CHECK(bg95_gpio_init());
    ESP_ERROR_CHECK(bg95_uart_init());

    bg95_enable_1v8_rail();

    if (bg95_probe_at(3)) {
        ESP_LOGI(TAG, "BG95 already responds; skipping PWRKEY pulse");
        bg95_run_at_smoke_test();
    } else {
        ESP_LOGW(TAG, "BG95 did not respond before power-on pulse");
        bg95_pulse_pwrkey();
        bg95_run_at_smoke_test();
    }

    ESP_LOGI(TAG, "BG95 bring-up loop active; leaving 1.8 V enabled and PWRKEY released.");

    int status_ms = 0;
    while (true) {
        const bool sim_sw_high = gpio_get_level(BG95_SIM_SW_GPIO) != 0;
        ESP_LOGI(TAG,
                 "1.8 V enable GPIO%d cmd=%d read=%d, PWRKEY GPIO%d cmd=%d read=%d, SIM_SW GPIO%d=%d",
                 BG95_1V8_EN_GPIO,
                 s_1v8_enable_commanded,
                 gpio_get_level(BG95_1V8_EN_GPIO),
                 BG95_PWRKEY_GPIO,
                 s_pwrkey_commanded,
                 gpio_get_level(BG95_PWRKEY_GPIO),
                 BG95_SIM_SW_GPIO,
                 sim_sw_high ? 1 : 0);
        vTaskDelay(pdMS_TO_TICKS(BG95_STATUS_LOG_MS));
        status_ms += BG95_STATUS_LOG_MS;

        if (status_ms >= BG95_AT_KEEPALIVE_MS) {
            status_ms = 0;
            ESP_LOGI(TAG, "Periodic BG95 AT keepalive");
            bg95_probe_at(1);
        }
    }
}
