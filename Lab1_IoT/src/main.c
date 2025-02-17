#include <stdio.h>
#include "freertos/FreeRTOS.h"
#include "freertos/task.h"
#include "driver/gpio.h"

static QueueHandle_t gpio_evt_queue = NULL;

#define GPIO_OUTPUT_IO 4
#define GPIO_INPUT_BUTT_IO 2
#define GPIO_OUTPUT_PIN_SEL (1ULL<<GPIO_OUTPUT_IO)
#define GPIO_OUTPUT_PIN_SEL_BUTT (1ULL<<GPIO_INPUT_BUTT_IO)

static void gpio_task_example(void* arg)
{
    uint32_t io_num;
    for (;;) {
        if (xQueueReceive(gpio_evt_queue, &io_num, portMAX_DELAY)) {
            printf("GPIO[%"PRIu32"] intr, val: %d\n", io_num, gpio_get_level(io_num));
        }
    }
}

void app_main() {
    //zero-initialize the config structure.
    gpio_config_t io_conf = {};
    //disable interrupt
    io_conf.intr_type = GPIO_INTR_DISABLE;
    //set as output mode
    io_conf.mode = GPIO_MODE_OUTPUT;
    //bit mask of the pins that you want to set
    io_conf.pin_bit_mask = GPIO_OUTPUT_PIN_SEL;
    //disable pull-down mode
    io_conf.pull_down_en = 0;
    //disable pull-up mode
    io_conf.pull_up_en = 0;
    //configure GPIO with the given settings
    gpio_config(&io_conf);

    //disable interrupt
    io_conf.intr_type = GPIO_INTR_POSEDGE;
    //set as output mode
    io_conf.mode = GPIO_MODE_INPUT;
    //bit mask of the pins that you want to set
    io_conf.pin_bit_mask = GPIO_OUTPUT_PIN_SEL_BUTT;
    //disable pull-down mode
    // io_conf.pull_down_en = 0;
    //disable pull-up mode
    io_conf.pull_up_en = 1;
    gpio_config(&io_conf);
    gpio_set_intr_type(GPIO_INPUT_BUTT_IO, GPIO_INTR_ANYEDGE);

    int cnt = 0;
    while(1) {
        // printf("cnt: %d\n", cnt++);
        // printf("1s\n");
        // gpio_set_level(GPIO_OUTPUT_IO, 1);
        // vTaskDelay(1000 / portTICK_PERIOD_MS);
        
        // printf("0.5s\n");
        // gpio_set_level(GPIO_OUTPUT_IO, 0);
        // vTaskDelay(500 / portTICK_PERIOD_MS);

        // printf("0.25s\n");
        // gpio_set_level(GPIO_OUTPUT_IO, 1);
        // vTaskDelay(250 / portTICK_PERIOD_MS);

        // printf("0.75s\n");
        // gpio_set_level(GPIO_OUTPUT_IO, 0);
        vTaskDelay(1000 / portTICK_PERIOD_MS);
        if(gpio_get_level(GPIO_INPUT_BUTT_IO) == 0){
            printf("cnt: %d\n", cnt++);

        }
    }
}