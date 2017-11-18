from humanplayer import HumanPlayer
from randomplayer import RandomPlayer
from qplayer import QPlayer

class PlayerFactory(object):

    @classmethod
    def create(self,bType,wType,QN,mode,num_episodes):
        """ Create player instance
        @param String bType
        @param String wType
        @param QNetwork QN
        @param String mode
        @param int num_episodes
        @return Player Player
        """
        b = QPlayer(1,QN,mode,num_episodes)
        w = QPlayer(-1,QN,mode,num_episodes)

        if bType == HumanPlayer.getType():
            b = HumanPlayer(1)
        elif bType == RandomPlayer.getType():
            b = RandomPlayer(1)

        if wType == HumanPlayer.getType():
            w = HumanPlayer(-1)
        elif wType == RandomPlayer.getType():
            w = RandomPlayer(-1)
        return b,w

    @classmethod
    def getTypes(self):
        """ Return all players types
        @return list(String) types
        """
        types = []
        types.append(HumanPlayer.getType())
        types.append(RandomPlayer.getType())
        types.append(QPlayer.getType())
        types.append("") #null argument
        return types
