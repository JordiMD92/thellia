python main.py -m load -e 100000 -n relu -b QP -w MP -r 0.0001 -d 0.4;
python main.py -m load -e 100000 -n reluLarge -b QP -w MP -r 0.0001 -d 0.4;
python main.py -m train -e 100000 -n relu -b QP -w MP -r 0.0001 -d 0.4;
python main.py -m train -e 100000 -n reluLarge -b QP -w MP -r 0.0001 -d 0.4;
python main.py -m train -e 100000 -n sigmoid -b QP -w MP -r 0.0001;
python main.py -m train -e 100000 -n tanh -b QP -w MP -r 0.0001;
