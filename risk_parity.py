import numpy as np
import pandas as pd
from scipy.optimize import differential_evolution


def risk_contribution(weights, cov):
    port_risk = np.sqrt(weights.T @ cov @ weights)
    rc = (cov @ weights) * weights / port_risk
    return rc

def target_risk_budget_func(weights, cov, target_risk_budget):
    weights = weights / np.sum(weights)
    rc = risk_contribution(weights, cov)
    rc_fraction = rc / np.sum(rc)
    return np.sum((rc_fraction - target_risk_budget) ** 2)


def optimize_risk_parity_scenario(data, asset_list, target_budget=None):
    returns = data[asset_list].pct_change().dropna()
    cov = returns.cov().values
    n = len(asset_list)
    if target_budget is None:
        target_budget = np.ones(n) / n

    result = differential_evolution(
        target_risk_budget_func,
        bounds=[(0, 1)] * n,
        args=(cov, target_budget),
    )
    w = result.x / np.sum(result.x)
    port_vol = np.sqrt(w @ cov @ w)
    return w, port_vol, cov


df = pd.read_excel('risk_parity_data.xlsx', parse_dates=["时间"])
df.columns = ["Date", "A", "B", "C"]
df.set_index("Date", inplace=True)
w1, vol1, cov1 = optimize_risk_parity_scenario(df, ['A', 'B'], target_budget=np.array([0.5, 0.5]))
w2, vol2, cov2 = optimize_risk_parity_scenario(df, ['A', 'B', 'C'], target_budget=np.array([1/3]*3))
print("Weights for s1 (A,B):", w1)
print("Weights for s2 (A,B,C):", w2)


returns = df.pct_change().dropna()
s1_returns = returns[['A', 'B']] @ w1
s2_returns = returns[['A', 'B', 'C']] @ w2

scenarios = pd.DataFrame({'s1':s1_returns, 's2':s2_returns})

cov_top = scenarios.cov().values
target_budget_top = np.array([1/2, 1/2])

result_top = differential_evolution(target_risk_budget_func, bounds=[(0, 1), (0, 1)], args=(cov_top, target_budget_top))
top_weights = result_top.x / np.sum(result_top.x)
print(top_weights)

final_weights = np.zeros(3)

final_weights[:2] += top_weights[0] * w1

final_weights += top_weights[1] * np.array([w2[0], w2[1], w2[2]])

final_weights /= np.sum(final_weights)

print(final_weights)

