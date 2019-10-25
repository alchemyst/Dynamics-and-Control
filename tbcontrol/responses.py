import numpy

def fopdt(t, K, tau, theta=0, y0=0):
    """ First Order Plus Dead Time response with bias

    Step response of
               K
    G(s) = ---------
           tau*s + 1

    :param t: time
    :param K: gain
    :param tau: time constant
    :param theta: dead time
    :param y0: bias
    """

    return y0 + numpy.sign(K)*numpy.maximum(0, abs(K)*(1 - numpy.exp(-(t - theta)/tau)))

def sopdt(t, K, tau, zeta, theta=0, y0=0):
    """ Second Order Plus Dead Time response with bias

    Step response of
                        K
    G(s) = --------------------------
           tau**2s + 2*tau*zeta*s + 1

    :param t: time
    :param K: gain
    :param tau: time constant
    :param zeta: damping coefficient
    :param theta: dead time
    :param y0: bias
    """

    tu = numpy.maximum(0, t - theta)  # undelayed time

    ttau = tu/tau
    exp = numpy.exp

    if zeta == 1:
        return y0 + K*(1 - (1 + ttau)*exp(-ttau))

    if zeta > 1:
        coslike = numpy.cosh
        sinlike = numpy.sinh
        root = numpy.sqrt(zeta**2 - 1)
    elif zeta < 1:
        coslike = numpy.cos
        sinlike = numpy.sin
        root = numpy.sqrt(1 - zeta**2)

    return y0 + K*(1 - exp(-zeta*ttau)*(coslike(root*ttau) 
                          + zeta/root*sinlike(root*ttau)))
