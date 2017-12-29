from relu import QNetworkRelu
from reluLarge import QNetworkReluLarge
from sigmoid import QNetworkSigmoid
from tanh import QNetworkTangent

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
        elif qType == QNetworkReluLarge.getType():
            return QNetworkReluLarge(lr,drop)
        elif qType == QNetworkTangent.getType():
            return QNetworkTangent(lr)
        else:
            return

    @classmethod
    def getTypes(self):
        """ Return all networks types
        @return list(String) types
        """
        types = []
        types.append(QNetworkRelu.getType())
        types.append(QNetworkReluLarge.getType())
        types.append(QNetworkSigmoid.getType())
        types.append(QNetworkTangent.getType())
        return types
