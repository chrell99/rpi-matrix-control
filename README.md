# rpi-matrix-control
Simple rpi hosted web app to control connected led signs using the [rpi-rgb-led-matrix](https://github.com/hzeller/rpi-rgb-led-matrix) library.

To create a virtual Python environment to run the code use the following command:
```
python3 -m venv env
```
To activate it 
```
source env/bin/activate
```
and to deactivate it
```
deactivate
```

Once the virtual environment has been activated, the required packages can be installed (while the virtual environment is active) with:
```
pip install -r requirements.txt
```


For now the only goal is to be able to control the video viewer, and some home made music sync binaries.

Command to compile video files to streams for better quality:
```
sudo /home/hoolacane/hoolacane-rpi-led-matrix/utils/video-viewer --led-chain=3 --led-parallel=3 --led-slowdown-gpio=2 --led-multiplexing=1 -T4 --led-pwm-bits=8 /home/hoolacane/media/TUNNEL_2.mp4 -O /home/hoolacane/TUNNEL_2_30p.stream --led-pixel-mapper="Rotate:270" --led-brightness=30
```

Command to show compiled stream file:
```
sudo /home/hoolacane/hoolacane-rpi-led-matrix/utils/led-image-viewer --led-chain=3 --led-parallel=3 --led-slowdown-gpio=2 --led-multiplexing=1 /home/hoolacane/streams/TUNNEL_2_30p.stream
```

Command to show the spectrum visualizer
```
sudo ./spectrum-visualizer 50 8000 100 35 7 1 0.9 1
```

TODO:
Roulette function
User sessions
Move files to folder and add to gitignore
Set lower limit for the visualizer and strobe to beat
Fix strobe to freq when average gets to close to current over time