import utest, hill

@utest.ok
def _check_is_backward():
    assert hill.isbackward("stop", "pots")