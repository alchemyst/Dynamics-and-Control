from tbcontrol.numeric import skogestad_half
import pytest

def test_skogestad_half_skogestad():
    # This is the example from
    # http://folk.ntnu.no/skoge/presentation/promatch-cybernetica-06/4tuning_short.pdf
    num_timeconstants = [-0.3, 0.08]
    den_timeconstants = [2, 1, 0.4, 0.2, 0.05, 0.05, 0.05]

    delay, timeconstants = skogestad_half(num_timeconstants, den_timeconstants, delay=0, order=1)

    assert delay == pytest.approx(1.47, 0.01)
    assert timeconstants[0] == pytest.approx(2.5)

    delay, timeconstants = skogestad_half(num_timeconstants, den_timeconstants, delay=0, order=2)

    assert delay == pytest.approx(0.77, 0.01)
    assert timeconstants[0] == pytest.approx(2)
    assert timeconstants[1] == pytest.approx(1.2)

def test_skogestad_half_seborg_ex5_4():
    # This is the example from seborg, Example 5.4
    num_timeconstants = [-0.1]
    den_timeconstants = [5, 3, 0.5]

    delay, timeconstants = skogestad_half(num_timeconstants, den_timeconstants, delay=0, order=1)

    assert delay == pytest.approx(2.1, 0.01)
    assert timeconstants[0] == pytest.approx(6.5)

def test_skogestad_half_seborg_ex5_5():
    # This is the example from seborg, Example 5.4
    num_timeconstants = [-1]
    den_timeconstants = [12, 3, 0.2, 0.05]

    delay, timeconstants = skogestad_half(num_timeconstants, den_timeconstants, delay=1, order=1)

    assert delay == pytest.approx(3.75, 0.01)
    assert timeconstants[0] == pytest.approx(13.5)

    delay, timeconstants = skogestad_half(num_timeconstants, den_timeconstants, delay=1, order=2)

    assert delay == pytest.approx(2.15, 0.01)
    assert timeconstants[0] == pytest.approx(12)
    assert timeconstants[1] == pytest.approx(3.1)
