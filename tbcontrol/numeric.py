import numpy

def skogestad_half(num_timeconstants, den_timeconstants, delay, order):
    """
    Approximate higher order transfer function using Skogestad's Half rule

    This method is specifically aimed at finding a first or second order
    plus dead time model of a transfer function.

    Note that the sign should be included in the time constant, so a term
    (s - 1) will have a time constant of 1, while a term (s + 1) will have a
    time constant of -1.

    :param num_timeconstants: numerator time constants
    :param den_timeconstants: denominator time constants
    :param delay: delay in original transfer function
    :param order: order of target transfer function
    :return approx_delay: delay time of approximation
    :return approx_timeconstants: time constants of approximation

    Reference: http://folk.ntnu.no/skoge/presentation/promatch-cybernetica-06/4tuning_short.pdf
    """

    if order > 2:
        raise NotImplementedError("Skogestad's rule is only meant for first or second order.")

    # Ensure time constants are in descending order
    den_timeconstants = numpy.sort(den_timeconstants)[::-1]

    if (den_timeconstants <= 0).any():
        raise ValueError("Skogestad's rule is meant for stable systems only.")

    approx_timeconstants = den_timeconstants[:order]
    neglected_constants = den_timeconstants[order:]

    approx_delay = delay + neglected_constants[0]/2 + sum(neglected_constants[1:]) - sum(num_timeconstants)
    approx_timeconstants[-1] += neglected_constants[0]/2

    return approx_delay, approx_timeconstants




