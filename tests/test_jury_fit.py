import numpy as np

from nj.jury import _fit_nonneg_l1, _platt
from nj.stats import auroc


def test_nonneg_l1_recovers_signal_and_ignores_noise():
    rng = np.random.default_rng(0)
    n = 600
    y = rng.integers(0, 2, n).astype(float)
    X = rng.normal(0, 1, (n, 6))
    X[:, 0] += 1.5 * y          # informative juror
    X[:, 1] += 0.8 * y          # weaker juror
    X[:, 2] -= 1.0 * y          # anti-correlated: must get weight 0 (non-negative constraint)
    w, b = _fit_nonneg_l1(X, y, 1e-3)
    assert (w >= 0).all()
    assert w[0] > w[1] > 0
    assert w[2] == 0
    s = X @ w + b
    assert auroc(s[y == 1], s[y == 0]) > 0.8
    a, c = _platt(s, y)
    assert a > 0
