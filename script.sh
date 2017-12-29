python main.py -m load -e 100000 -n relu -r 0.0001 -b QP -w MP -d 0.4;
python main.py -m train -e 100000 -n relu -r 0.0001 -b QP -w MP -d 0.4;
python main.py -m train -e 480000 -n relu -r 0.0001 -b QP -w MP -d 0.4;
