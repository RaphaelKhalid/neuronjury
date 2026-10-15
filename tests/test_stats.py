import numpy as np

from nj.stats import auroc, bh, control_game, paired_auroc_matrix, threshold_at_fpr, tpr_at


def test_auroc_basic():
    assert auroc([3, 4], [1, 2]) == 1.0
    assert auroc([1, 2], [3, 4]) == 0.0
    assert auroc([1, 1], [1, 1]) == 0.5
    rng = np.random.default_rng(0)
    a, b = rng.normal(1, 1, 4000), rng.normal(0, 1, 4000)
    assert abs(auroc(a, b) - 0.760) < 0.02  # Phi(1/sqrt2)


def test_paired_and_bh():
    att = np.array([[2, 0], [3, 0], [4, 1]])
    hon = np.array([[1, 0], [1, 0], [1, 1]])
    assert np.allclose(paired_auroc_matrix(att, hon), [1.0, 0.5])
    p = np.array([0.001, 0.01, 0.04, 0.5])
    assert bh(p, 0.05).tolist() == [True, True, False, False]


def test_threshold_and_tpr():
    hon = np.arange(100)
    tau = threshold_at_fpr(hon, 0.02)
    assert (hon > tau).mean() <= 0.02
    assert tpr_at([200, 0], tau) == 0.5


def test_control_game_extremes():
    hon = np.zeros(1000)
    caught = control_game(hon, np.full(50, 10.0), np.ones(50, bool), trials=200)
    assert caught["safety"] == 1.0
    missed = control_game(hon, np.full(50, -1.0), np.ones(50, bool), trials=200)
    assert missed["safety"] < 0.05
    harmless = control_game(hon, np.full(50, -1.0), np.zeros(50, bool), trials=200)
    assert harmless["safety"] == 1.0
