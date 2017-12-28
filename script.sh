python main.py -m load -e 100000 -n relu -r 0.0001 -b QP -w MP;
python main.py -m train -e 100000 -n relu -r 0.0001 -b QP -w MP;
python main.py -m load -e 100000 -n sigmoid -r 0.0001 -b QP -w MP;
python main.py -m train -e 100000 -n sigmoid -r 0.0001 -b QP -w MP;
