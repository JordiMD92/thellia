from qnetwork_relu import QNetworkRelu
from qnetwork_sigmoid import QNetworkSigmoid
from qnetwork_reluSM import QNetworkReluSM
from qnetwork_sigmoidSM import QNetworkSigmoidSM

class QNetworkFactory(object):

    @classmethod
    def create(self,qType,lr,drop):
        """ Create network instance
        @param String qType
        @return QNetwork QNetwork
        """
        if qType == QNetworkRelu.getType():
            return QNetworkRelu(lr,drop)
        elif qType == QNetworkSigmoid.getType():
            return QNetworkSigmoid(lr)
        elif qType == QNetworkReluSM.getType():
            return QNetworkReluSM(lr,drop)
        elif qType == QNetworkSigmoidSM.getType():
            return QNetworkSigmoidSM(lr)
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
        types.append(QNetworkReluSM.getType())
        types.append(QNetworkSigmoidSM.getType())
        return types
