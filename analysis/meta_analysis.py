from pathlib import Path
import numpy as np
import pandas as pd
from scipy.optimize import brentq
from scipy.stats import t

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / 'data'


def reml_hk(y, se):
    y = np.asarray(y, dtype=float)
    v = np.asarray(se, dtype=float) ** 2
    k = len(y)

    def score(tau2):
        w = 1.0 / (v + tau2)
        mu = np.sum(w * y) / np.sum(w)
        return np.sum(w**2 * ((y - mu)**2 - (v + tau2)))

    if score(0.0) <= 0:
        tau2 = 0.0
    else:
        hi = 1.0
        while score(hi) > 0:
            hi *= 2.0
        tau2 = brentq(score, 0.0, hi)

    w = 1.0 / (v + tau2)
    mu = np.sum(w * y) / np.sum(w)
    q_re = np.sum(w * (y - mu)**2)
    se_conv = np.sqrt(1.0 / np.sum(w))
    # Modified Hartung-Knapp (variance inflation not allowed below conventional RE variance)
    q_star = max(1.0, q_re / (k - 1))
    se_hk = np.sqrt(q_star / np.sum(w))
    crit = t.ppf(0.975, k - 1)
    ci = (mu - crit * se_hk, mu + crit * se_hk)

    w0 = 1.0 / v
    mu0 = np.sum(w0 * y) / np.sum(w0)
    Q = np.sum(w0 * (y - mu0)**2)
    I2 = max(0.0, (Q - (k - 1)) / Q) * 100.0 if Q > 0 else 0.0
    pred_se = np.sqrt(tau2 + se_hk**2)
    pred = (mu - crit * pred_se, mu + crit * pred_se)
    return dict(k=k, mean=mu, se_hk=se_hk, ci_low=ci[0], ci_high=ci[1], tau2=tau2, I2=I2, Q=Q, pred_low=pred[0], pred_high=pred[1])


def main():
    arch = pd.read_csv(DATA / 'architecture_effects.csv')
    delayed = pd.read_csv(DATA / 'delayed_retention_effects.csv')
    rows = []
    for label, frame in arch.groupby('architecture', sort=False):
        rows.append({'analysis': label, **reml_hk(frame.effect, frame.se)})
    rows.append({'analysis': 'Delayed retention primary', **reml_hk(delayed.effect, delayed.se)})
    rows.append({'analysis': 'Delayed retention without Barcaui', **reml_hk(delayed.loc[~delayed.study.str.contains('Barcaui'), 'effect'], delayed.loc[~delayed.study.str.contains('Barcaui'), 'se'])})
    out = pd.DataFrame(rows)
    print(out.to_string(index=False))


if __name__ == '__main__':
    main()
