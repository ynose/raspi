require 'wiringpi2'

# BCMのGPIO番号からWiringpi-Rubyピン番号への変換関数（旧モデルB用）
def gpio_pin_to_wpi_pin(pin)
  wpi_pins = {
     2 =>  8,
     3 =>  9,
     4 =>  7,
     7 => 11,
     8 => 10,
     9 => 13,
    10 => 12,
    11 => 14,
    14 => 15,
    15 => 16,
    17 =>  0,
    18 =>  1,
    22 =>  3,
    23 =>  4,
    24 =>  5,
    25 =>  6,
    27 =>  2,
    28 => 17,
    29 => 18,
    30 => 19,
    31 => 20
  }
  if wpi_pins.has_key?(pin) then
    return wpi_pins[pin]
  else
    raise "gpio_pin error"
  end
end

# BCMのGPIOピン番号
gpio_number = 25
# 点滅の間隔[sec]
interval = 1
# Wiringpi-Rubyピン番号の取得
pin = gpio_pin_to_wpi_pin(gpio_number)
# GPIOクラスのインスタンス生成
gpio = WiringPi::GPIO.new
# GPIO 8ピンの入出力方向を出力に設定
gpio.pin_mode(pin, WiringPi::OUTPUT)
# 点灯はWiringPi::HIGH（実際の値は1）
value = WiringPi::HIGH
# 10回繰り返し
10.times do
  # valueの値をGPIO 8ピンへ設定
  gpio.digital_write(pin, value)
  # GPIO 8ピンの値を取得
  v = gpio.digital_read(pin)
  # GPIO 8ピンの値をコンソールへ出力
  puts v
  # interval秒一時休止
  sleep(interval)
  # 点滅させるため、HIGHとLOWの値を入れ替える
  if value == WiringPi::HIGH then
    value = WiringPi::LOW # 消灯はWiringPi::LOW（実際の値は0）
  else
    value = WiringPi::HIGH
  end
end
