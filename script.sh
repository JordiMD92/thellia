python main.py -m load -e 100000 -n relu -b QP -w MP -r 0.0001 -d 1.0;
python main.py -m load -e 100000 -n reluLarge -b QP -w MP -r 0.0001 -d 1.0;
python main.py -m train -e 100000 -n relu -b QP -w MP -r 0.0001 -d 1.0;
python main.py -m train -e 100000 -n reluLarge -b QP -w MP -r 0.0001 -d 1.0;
