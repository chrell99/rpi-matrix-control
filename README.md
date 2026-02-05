# rpi-matrix-control
Simple rpi hosted web app to control connected led signs using the [rpi-rgb-led-matrix](https://github.com/hzeller/rpi-rgb-led-matrix) library.

For now the only goal is to be able to control the video viewer, and some home made music sync binaries.

Command to compile video files to streams for better quality:
```
cd /home/hoolacane/hoolacane-rpi-led-matrix/utils && sudo ./video-viewer --led-chain=3 --led-parallel=3 --led-slowdown-gpio=2 --led-multiplexing=1 -T4 --led-pwm-bits=8 ../img/{video}.mp4 -O{RPIcmd.stream}{video}.stream --led-pixel-mapper="Rotate:90"
```






