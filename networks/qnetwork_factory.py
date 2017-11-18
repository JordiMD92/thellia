from qnetwork_relu import QNetworkRelu
from qnetwork_sigmoid import QNetworkSigmoid

class QNetworkFactory(object):

    @classmethod
    def create(self,qType):
        """ Create network instance
        @param String qType
        @return QNetwork QNetwork
        """
        if qType == QNetworkRelu.getType():
            return QNetworkRelu()
        elif qType == QNetworkSigmoid.getType():
            return QNetworkSigmoid()
        else:
            return

    @classmethod
    def getTypes(self):
        """ Return all networks types
        @return list(String) types
        """
        types = []
        types.append(QNetworkRelu.getType())
        types.append(QNetworkSigmoid.getType())
        return types
