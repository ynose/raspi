require 'wiringpi2'
require 'pp'

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

gpio = WiringPi::GPIO.new
gpio_pins = [2, 3, 4, 7, 8, 9, 10, 11, 14, 15, 17, 18, 22, 23, 24, 25, 27, 28, 29, 30, 31]
pins = Hash.new
gpio_pins.each do |gpio_pin|
  wpi_pin = gpio_pin_to_wpi_pin(gpio_pin)
  pins[gpio_pin] = gpio.digital_read(wpi_pin)
end
pins.each do |pin|
  pp pin
end
