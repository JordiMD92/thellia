from qnetwork_relu import QNetworkRelu
from qnetwork_sigmoid import QNetworkSigmoid
from qnetwork_softmax import QNetworkSoftmax

class QNetworkFactory(object):

    @classmethod
    def create(self,qType,batch_size):
        """ Create network instance
        @param String qType
        @return QNetwork QNetwork
        """
        if qType == QNetworkRelu.getType():
            return QNetworkRelu(batch_size)
        elif qType == QNetworkSigmoid.getType():
            return QNetworkSigmoid(batch_size)
        elif qType == QNetworkSoftmax.getType():
            return QNetworkSoftmax(batch_size)
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
        types.append(QNetworkSoftmax.getType())
        return types
