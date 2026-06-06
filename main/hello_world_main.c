/*
 * OLED bring-up test for ER-OLED018-1 / SSD1326 over I2C.
 */

#include <stdbool.h>
#include <stdint.h>
#include <string.h>

#include "driver/gpio.h"
#include "driver/i2c_master.h"
#include "esp_check.h"
#include "esp_err.h"
#include "esp_log.h"
#include "freertos/FreeRTOS.h"
#include "freertos/task.h"

#define OLED_WIDTH 256
#define OLED_HEIGHT 32
#define OLED_BYTES_PER_ROW (OLED_WIDTH / 2)
#define OLED_FRAME_BYTES (OLED_BYTES_PER_ROW * OLED_HEIGHT)

#define OLED_SDA_GPIO GPIO_NUM_11
#define OLED_SCL_GPIO GPIO_NUM_10
#define OLED_RST_GPIO GPIO_NUM_9
#define R1200_CE_GPIO GPIO_NUM_8
#define R1200_PWR_EN_GPIO GPIO_NUM_18

#define OLED_I2C_PORT I2C_NUM_0
#define OLED_I2C_SPEED_HZ 100000

#define OLED_RST_ACTIVE_LEVEL 0
#define R1200_CE_ENABLE_LEVEL 1
#define R1200_PWR_ENABLE_LEVEL 1

#define OLED_I2C_TIMEOUT_MS 1000
#define OLED_POWER_STARTUP_DELAY_MS 3000
#define OLED_POWER_STEP_DELAY_MS 5000
#define OLED_ENABLE_R1200_CE 1

static const char *TAG = "oled_test";

static i2c_master_bus_handle_t s_i2c_bus;
static i2c_master_dev_handle_t s_oled;
static uint8_t s_framebuffer[OLED_FRAME_BYTES];

static int iabs_int(int value)
{
    return value < 0 ? -value : value;
}

static uint8_t max_u8(uint8_t a, uint8_t b)
{
    return a > b ? a : b;
}

static void oled_set_reset(bool asserted)
{
    gpio_set_level(OLED_RST_GPIO, asserted ? OLED_RST_ACTIVE_LEVEL : !OLED_RST_ACTIVE_LEVEL);
}

static void r1200_set_ce(bool enabled)
{
    gpio_set_level(R1200_CE_GPIO, enabled ? R1200_CE_ENABLE_LEVEL : !R1200_CE_ENABLE_LEVEL);
}

static void r1200_set_power_enable(bool enabled)
{
    gpio_set_level(R1200_PWR_EN_GPIO, enabled ? R1200_PWR_ENABLE_LEVEL : !R1200_PWR_ENABLE_LEVEL);
}

static esp_err_t board_gpio_init(void)
{
    gpio_config_t output_config = {
        .pin_bit_mask = (1ULL << OLED_RST_GPIO) |
                        (1ULL << R1200_CE_GPIO) |
                        (1ULL << R1200_PWR_EN_GPIO),
        .mode = GPIO_MODE_OUTPUT,
        .pull_up_en = GPIO_PULLUP_DISABLE,
        .pull_down_en = GPIO_PULLDOWN_DISABLE,
        .intr_type = GPIO_INTR_DISABLE,
    };

    ESP_RETURN_ON_ERROR(gpio_config(&output_config), TAG, "GPIO output config failed");

    r1200_set_ce(false);
    r1200_set_power_enable(false);
    oled_set_reset(true);

    return ESP_OK;
}

static esp_err_t oled_i2c_bus_init(void)
{
    i2c_master_bus_config_t bus_config = {
        .clk_source = I2C_CLK_SRC_DEFAULT,
        .i2c_port = OLED_I2C_PORT,
        .scl_io_num = OLED_SCL_GPIO,
        .sda_io_num = OLED_SDA_GPIO,
        .glitch_ignore_cnt = 7,
        .flags.enable_internal_pullup = true,
    };

    return i2c_new_master_bus(&bus_config, &s_i2c_bus);
}

static void oled_detach_device(void)
{
    if (s_oled != NULL) {
        esp_err_t ret = i2c_master_bus_rm_device(s_oled);
        if (ret != ESP_OK) {
            ESP_LOGW(TAG, "OLED I2C detach failed: %s", esp_err_to_name(ret));
        }

        s_oled = NULL;
    }
}

static void oled_log_i2c_scan(void)
{
    bool found_any = false;

    for (uint8_t address = 0x08; address < 0x78; address++) {
        if (i2c_master_probe(s_i2c_bus, address, 50) == ESP_OK) {
            ESP_LOGW(TAG, "I2C device ACK at 0x%02x", address);
            found_any = true;
        }
    }

    if (!found_any) {
        ESP_LOGW(TAG, "No I2C devices ACKed on GPIO%d/GPIO%d", OLED_SDA_GPIO, OLED_SCL_GPIO);
    }
}

static esp_err_t oled_attach_device(void)
{
    if (s_oled != NULL) {
        return ESP_OK;
    }

    const uint8_t address_candidates[] = {
        0x3C, // Datasheet 0x78 when SA0 = 0.
        0x3D, // Datasheet 0x7A when SA0 = 1.
    };

    uint8_t address = 0;
    for (size_t i = 0; i < sizeof(address_candidates); i++) {
        esp_err_t probe_ret = i2c_master_probe(s_i2c_bus, address_candidates[i], 100);
        if (probe_ret == ESP_OK) {
            address = address_candidates[i];
            break;
        }
    }

    if (address == 0) {
        ESP_LOGE(TAG, "OLED did not ACK at 0x3C or 0x3D");
        return ESP_ERR_NOT_FOUND;
    }

    i2c_device_config_t dev_config = {
        .dev_addr_length = I2C_ADDR_BIT_LEN_7,
        .device_address = address,
        .scl_speed_hz = OLED_I2C_SPEED_HZ,
    };

    ESP_LOGI(TAG, "OLED ACKed at I2C address 0x%02x", address);
    return i2c_master_bus_add_device(s_i2c_bus, &dev_config, &s_oled);
}

static void oled_power_on_sequence(void)
{
    ESP_LOGI(TAG, "OLED power step: assert reset low, keep 12V path disabled");
    oled_set_reset(true);
    vTaskDelay(pdMS_TO_TICKS(OLED_POWER_STEP_DELAY_MS));

    ESP_LOGI(TAG, "OLED power step: set GPIO%d R1200_PWR_EN active", R1200_PWR_EN_GPIO);
    r1200_set_power_enable(true);
    vTaskDelay(pdMS_TO_TICKS(OLED_POWER_STEP_DELAY_MS));

#if OLED_ENABLE_R1200_CE
    ESP_LOGI(TAG, "OLED power step: set GPIO%d R1200_CE active", R1200_CE_GPIO);
    r1200_set_ce(true);
    vTaskDelay(pdMS_TO_TICKS(OLED_POWER_STEP_DELAY_MS));
#else
    ESP_LOGW(TAG, "Diagnostic hold: GPIO%d R1200_CE is kept disabled to prevent brownout/reset",
             R1200_CE_GPIO);
    while (true) {
        vTaskDelay(pdMS_TO_TICKS(1000));
    }
#endif

    ESP_LOGI(TAG, "OLED power step: release OLED reset on GPIO%d", OLED_RST_GPIO);
    oled_set_reset(false);
    vTaskDelay(pdMS_TO_TICKS(100));
}

static esp_err_t oled_write_commands(const uint8_t *commands, size_t command_count)
{
    uint8_t tx[64];

    if (command_count > sizeof(tx) - 1) {
        return ESP_ERR_INVALID_SIZE;
    }

    tx[0] = 0x00;
    memcpy(&tx[1], commands, command_count);
    return i2c_master_transmit(s_oled, tx, command_count + 1, OLED_I2C_TIMEOUT_MS);
}

static esp_err_t oled_write_command1(uint8_t command)
{
    return oled_write_commands(&command, 1);
}

static esp_err_t oled_set_window(void)
{
    const uint8_t commands[] = {
        0x15, 0x00, 0x7F,
        0x75, 0x00, 0x1F,
    };

    return oled_write_commands(commands, sizeof(commands));
}

static esp_err_t oled_send_frame(void)
{
    uint8_t data_control = 0x40;
    i2c_master_transmit_multi_buffer_info_t buffers[] = {
        {
            .write_buffer = &data_control,
            .buffer_size = sizeof(data_control),
        },
        {
            .write_buffer = s_framebuffer,
            .buffer_size = sizeof(s_framebuffer),
        },
    };

    ESP_RETURN_ON_ERROR(oled_set_window(), TAG, "set display window failed");
    return i2c_master_multi_buffer_transmit(s_oled, buffers, 2, OLED_I2C_TIMEOUT_MS);
}

static esp_err_t oled_init_controller(void)
{
    const uint8_t init_commands[] = {
        0xFD, 0x12,       // Command lock off.
        0xAE,             // Display off while the RAM is initialized.
        0x15, 0x00, 0x7F, // 128 byte columns = 256 grayscale pixels.
        0x75, 0x00, 0x1F, // 32 rows.
        0x81, 0x27,       // Contrast current from the module datasheet.
        0x87,             // Current range.
        0xA0, 0x07,       // Remap and grayscale mode.
        0xA1, 0x00,       // Display start line.
        0xA2, 0x00,       // Display offset.
        0xA8, 0x1F,       // 1/32 mux.
        0xB1, 0x71,       // Phase length.
        0xB3, 0xF0,       // Clock divider / oscillator.
        0xB7,             // Default linear grayscale table.
        0xBB, 0x35, 0xFF, // Pre-charge setup.
        0xBC, 0x1F,       // Pre-charge voltage.
        0xBE, 0x0F,       // VCOMH.
    };

    ESP_RETURN_ON_ERROR(oled_write_commands(init_commands, sizeof(init_commands)), TAG, "SSD1326 init failed");

    memset(s_framebuffer, 0, sizeof(s_framebuffer));
    ESP_RETURN_ON_ERROR(oled_send_frame(), TAG, "clear frame failed");
    ESP_RETURN_ON_ERROR(oled_write_command1(0xAF), TAG, "display on failed");
    vTaskDelay(pdMS_TO_TICKS(100));

    return ESP_OK;
}

static void framebuffer_set_pixel(int x, int y, uint8_t gray)
{
    if (x < 0 || x >= OLED_WIDTH || y < 0 || y >= OLED_HEIGHT) {
        return;
    }

    gray &= 0x0F;
    uint8_t *byte = &s_framebuffer[(y * OLED_BYTES_PER_ROW) + (x / 2)];

    if ((x & 1) == 0) {
        *byte = (*byte & 0x0F) | (gray << 4);
    } else {
        *byte = (*byte & 0xF0) | gray;
    }
}

static void framebuffer_fill(uint8_t gray)
{
    gray &= 0x0F;
    memset(s_framebuffer, (gray << 4) | gray, sizeof(s_framebuffer));
}

static void framebuffer_rect(int x0, int y0, int width, int height, uint8_t gray)
{
    for (int y = y0; y < y0 + height; y++) {
        for (int x = x0; x < x0 + width; x++) {
            framebuffer_set_pixel(x, y, gray);
        }
    }
}

static void framebuffer_draw_border(uint8_t gray)
{
    for (int x = 0; x < OLED_WIDTH; x++) {
        framebuffer_set_pixel(x, 0, gray);
        framebuffer_set_pixel(x, OLED_HEIGHT - 1, gray);
    }

    for (int y = 0; y < OLED_HEIGHT; y++) {
        framebuffer_set_pixel(0, y, gray);
        framebuffer_set_pixel(OLED_WIDTH - 1, y, gray);
    }
}

static void render_startup_animation_frame(int frame)
{
    const int bright_center = (frame * 6) % (OLED_WIDTH + 64) - 32;
    const int dim_center = OLED_WIDTH - 1 - ((frame * 4) % OLED_WIDTH);

    framebuffer_fill(0);

    for (int y = 0; y < OLED_HEIGHT; y++) {
        for (int x = 0; x < OLED_WIDTH; x++) {
            uint8_t gray = (uint8_t)(((x / 16) + (y / 8) + (frame / 6)) & 0x01);

            int bright_distance = iabs_int(x - bright_center);
            if (bright_distance < 48) {
                gray = max_u8(gray, (uint8_t)(15 - (bright_distance / 4)));
            }

            int dim_distance = iabs_int(x - dim_center);
            if (dim_distance < 24) {
                gray = max_u8(gray, (uint8_t)(8 - (dim_distance / 3)));
            }

            if (((x + (frame * 3) + (y * 6)) % 48) < 3) {
                gray = max_u8(gray, 10);
            }

            framebuffer_set_pixel(x, y, gray);
        }
    }

    framebuffer_draw_border(15);
}

static void render_idle_test_frame(int frame)
{
    framebuffer_fill(0);

    for (int y = 0; y < OLED_HEIGHT; y++) {
        for (int x = 0; x < OLED_WIDTH; x++) {
            uint8_t gray = (uint8_t)((x + frame) & 0x0F);

            if (((x + frame) % 64) < 6) {
                gray = 15;
            }

            if (((x / 8) ^ (y / 4) ^ (frame / 8)) & 0x01) {
                gray = max_u8(gray, 3);
            }

            framebuffer_set_pixel(x, y, gray);
        }
    }

    framebuffer_rect(8, 8, 5, 16, 15);
    framebuffer_rect(13, 8, 14, 4, 15);
    framebuffer_rect(13, 20, 14, 4, 15);
    framebuffer_rect(27, 8, 5, 16, 15);

    framebuffer_rect(42, 8, 5, 16, 15);
    framebuffer_rect(47, 20, 18, 4, 15);

    framebuffer_rect(75, 8, 5, 16, 15);
    framebuffer_rect(80, 8, 18, 4, 15);
    framebuffer_rect(80, 14, 14, 4, 12);
    framebuffer_rect(80, 20, 18, 4, 15);

    framebuffer_rect(108, 8, 5, 16, 15);
    framebuffer_rect(113, 8, 14, 4, 15);
    framebuffer_rect(113, 20, 14, 4, 15);
    framebuffer_rect(127, 12, 5, 8, 15);

    framebuffer_draw_border(15);
}

static esp_err_t run_startup_animation(void)
{
    for (int frame = 0; frame < 70; frame++) {
        render_startup_animation_frame(frame);
        ESP_RETURN_ON_ERROR(oled_send_frame(), TAG, "startup animation frame failed");
        vTaskDelay(pdMS_TO_TICKS(18));
    }

    return ESP_OK;
}

void app_main(void)
{
    ESP_LOGI(TAG, "Starting ER-OLED018-1 SSD1326 I2C test");

    esp_err_t ret = board_gpio_init();
    if (ret != ESP_OK) {
        ESP_LOGE(TAG, "GPIO init failed: %s", esp_err_to_name(ret));
        while (true) {
            vTaskDelay(pdMS_TO_TICKS(1000));
        }
    }

    ret = oled_i2c_bus_init();
    if (ret != ESP_OK) {
        ESP_LOGE(TAG, "I2C bus init failed: %s", esp_err_to_name(ret));
        while (true) {
            vTaskDelay(pdMS_TO_TICKS(1000));
        }
    }

    ESP_LOGI(TAG, "Holding OLED 12V rail off for %d ms before first enable",
             OLED_POWER_STARTUP_DELAY_MS);
    vTaskDelay(pdMS_TO_TICKS(OLED_POWER_STARTUP_DELAY_MS));

    bool oled_ready = false;

    int frame = 0;
    while (true) {
        if (!oled_ready) {
            oled_power_on_sequence();

            ret = oled_attach_device();
            if (ret != ESP_OK) {
                ESP_LOGW(TAG, "OLED not ready yet: %s", esp_err_to_name(ret));
                oled_log_i2c_scan();
                vTaskDelay(pdMS_TO_TICKS(1000));
                continue;
            }

            ret = oled_init_controller();
            if (ret != ESP_OK) {
                ESP_LOGW(TAG, "OLED init failed: %s", esp_err_to_name(ret));
                oled_detach_device();
                vTaskDelay(pdMS_TO_TICKS(1000));
                continue;
            }

            ret = run_startup_animation();
            if (ret != ESP_OK) {
                ESP_LOGW(TAG, "OLED startup animation failed: %s", esp_err_to_name(ret));
                oled_detach_device();
                vTaskDelay(pdMS_TO_TICKS(1000));
                continue;
            }

            oled_ready = true;
        }

        render_idle_test_frame(frame++);
        ret = oled_send_frame();
        if (ret != ESP_OK) {
            ESP_LOGW(TAG, "OLED frame write failed: %s", esp_err_to_name(ret));
            oled_detach_device();
            oled_ready = false;
            vTaskDelay(pdMS_TO_TICKS(1000));
            continue;
        }

        vTaskDelay(pdMS_TO_TICKS(45));
    }
}
