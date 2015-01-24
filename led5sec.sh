#GPIO25に接続したLEDを5秒間点灯する
gpio_number=25
echo "${gpio_number}" > /sys/class/gpio/export
echo "out" > /sys/class/gpio/gpio${gpio_number}/direction
echo "1" > /sys/class/gpio/gpio${gpio_number}/value
sleep 5
echo "0" > /sys/class/gpio/gpio${gpio_number}/value
echo "${gpio_number}" > /sys/class/gpio/unexport
