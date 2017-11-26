from qnetwork_relu import QNetworkRelu
from qnetwork_sigmoid import QNetworkSigmoid
from qnetwork_reluSM import QNetworkReluSM
from qnetwork_sigmoidSM import QNetworkSigmoidSM

class QNetworkFactory(object):

    @classmethod
    def create(self,qType,batch_size,lr,drop):
        """ Create network instance
        @param String qType
        @return QNetwork QNetwork
        """
        if qType == QNetworkRelu.getType():
            return QNetworkRelu(batch_size,lr,drop)
        elif qType == QNetworkSigmoid.getType():
            return QNetworkSigmoid(batch_size,lr)
        elif qType == QNetworkReluSM.getType():
            return QNetworkReluSM(batch_size,lr,drop)
        elif qType == QNetworkSigmoidSM.getType():
            return QNetworkSigmoidSM(batch_size,lr)
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
