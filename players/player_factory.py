from humanplayer import HumanPlayer
from randomplayer import RandomPlayer
from maxtileplayer import MaxTilePlayer
from qplayer import QPlayer

class PlayerFactory(object):

    @classmethod
    def create(self,view,bType,wType,QN,targetQN,mode,num_episodes):
        """ Create player instance
        @param String bType
        @param String wType
        @param QNetwork QN
        @param String mode
        @param int num_episodes
        @return Player Player
        """
        b = QPlayer(1,QN,targetQN,mode,num_episodes,train=True)
        w = QPlayer(-1,QN,targetQN,mode,num_episodes,train=False)

        if bType == HumanPlayer.getType():
            b = HumanPlayer(1,view)
        elif bType == RandomPlayer.getType():
            b = RandomPlayer(1)
        elif bType == MaxTilePlayer.getType():
            b = MaxTilePlayer(1)

        if wType == HumanPlayer.getType():
            w = HumanPlayer(-1,view)
        elif wType == RandomPlayer.getType():
            w = RandomPlayer(-1)
        elif wType == MaxTilePlayer.getType():
            w = MaxTilePlayer(-1)

        return b,w

    @classmethod
    def getTypes(self):
        """ Return all players types
        @return list(String) types
        """
        types = []
        types.append(HumanPlayer.getType())
        types.append(RandomPlayer.getType())
        types.append(MaxTilePlayer.getType())
        types.append(QPlayer.getType())
        types.append("") #null argument
        return types
