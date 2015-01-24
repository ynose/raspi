# raspi
Raspberry Piの練習プログラム

led5sec.sh  
５秒間LEDを転送するサンプル

led5sec.rb  
Rubyからled5sec.shを呼び出すサンプル

led5blink.rb  
５回LEDを点滅するサンプル(Ruby)

  以下の手順が必要
  bundlerをインストール  
  $ sudo apt-get install bundler

  wiringpi2をインストール
  $ bundle install --path vendor/bundle

  実行方法
  $ sudo bundle exec ruby led10blink.rb
