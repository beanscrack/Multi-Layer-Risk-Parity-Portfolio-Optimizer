📊 Risk Parity Portfolio Optimizer

This project implements a multi-scenario **risk parity portfolio construction framework** in Python. It uses historical return data and optimizes asset weights such that each component contributes proportionally to the overall portfolio risk, based on a target risk budget. The model further blends multiple portfolio scenarios using an additional risk parity optimization layer — a practical method often seen in real-world portfolio construction.

🧠 Concept

**Risk Parity** is a portfolio allocation strategy that assigns weights to assets based on their risk contributions, rather than expected returns. This approach is particularly useful in volatile or uncertain market environments where traditional return forecasts may be unreliable.

This implementation goes a step further:
- Builds **individual scenario portfolios** (e.g., A&B vs A,B,C)
- Combines those portfolios into a **top-level allocation** using another layer of risk parity optimization

🚀 How It Works

1. **Input**: Time series price data (Excel format)
2. **Processing**:
   - Convert prices to returns
   - Compute covariance matrix
   - Optimize portfolio weights via Differential Evolution to match a target risk budget
3. **Multi-Layer Allocation**:
   - Two portfolio “scenarios” are created:
     - Scenario 1: Assets A & B with 50/50 risk budget
     - Scenario 2: Assets A, B, & C with equal risk contributions
   - Final weights are calculated by combining both scenarios using another risk-parity layer
4. **Output**:
   - Asset-level weights
   - Portfolio-level volatility
   - Risk contributions

📦 Dependencies

- Python 3.8+
- `numpy`
- `pandas`
- `scipy`
- `openpyxl` (for reading `.xlsx` files)

Install dependencies with:

```bash
pip install -r requirements.txt

