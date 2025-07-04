# twap_strategy_optimiser_app
This is an interactive Plotly Dash web application that computes and visualises an optimised Time-Weighted Average Price (TWAP) execution schedule. The optimiser is grounded in stochastic control theory subject to fast trading and terminal inventory penalties, and dynamically calculates how much of an order to execute at each time interval to minimise expected costs.
This web app provides an interactive interface to visualise and explore a Time-Weighted Average Price (TWAP) execution strategy optimised via stochastic control and dynamic programming. It is built using Plotly Dash and is designed to assist traders, quants, and researchers in understanding optimal execution schedules under stochastic price dynamics.

This app is the result of a stochastic control problem solved as part of my university coursework. The objective was to optimally execute a large order over time in a way that accounts for both market impact and price uncertainty.

The problem was solved using an ansatz to simplify the stochastic control problem, and the dynamic programming principle in the context of the Hamilton-Jacobi-Bellman (HJB) equation to derive optimal control, and a finite-horizon model ensuring the complete execution by the final time step subject to inventory penalties. The resulting policy determines how much to trade at each discrete time interval.

Features include:
  - Live stock price integration using Yahoo Finance: Select your preferred stock ticker directly in the app. Live mid-price data is fetched and used to compute basline TWAP.
  - Interactive Visualisations built with Plotly: Optimised execution schedule vs standard TWAP.
  - Fully interpretable execution logic based on rigorous control-theoretic principles.
  - Parameter customisation: Time Horizon, Inventory Level, Volatility, Impact Coefficients, etc.

Mathematical Model:
  -  A stochastic price process
  -  Market impact, execution cost (trading speed penalty)
  -  Objective: Minimise expected total execution cost
  -  Contraint: Inventory volume and terminal penalty

Consider Price Dynamics:

$dQ_t = \nu_t dt$,

$dS_t = b\nu_t dt + \sigma dW_t$,

$dX_t = -(S_t + k\nu_t)\nu_t dt$


Performance Criterion:

$J^{\nu}(X_0, Q_0, S_0) = \mathbb{E} [ X_T + Q_T(S_T - \alpha Q_T)], \alpha > 0$

Dynamic Value Function:

$H(t, X_t, Q_t, S_t) = \sup_{\nu} \mathbb{E} [X_T + Q_T(S_T - \alpha Q_T) \vert \mathrm{F}]$

Where $\mathrm{F}$ is the filtration at time t. 

Using the Ansatz: 

$H(t, X, Q, S) = X + QS + h(t,Q)$

We arrive at the optimal control $\nu^{*}$.

$\nu^{*}(t,Q) = \frac{-(2\alpha - b)}{2k + (2\alpha - b)(T-t)} Q$

After substituing $\nu^{*}$ back into $dQ_t = \nu_t dt$,

we get,

$Q_t = \frac{2k + (2\alpha-b)(T-t)}{2k+(2\alpha-b)T}Q_0$.

After some mental gymnastics, consider the limit when $\alpha -> infinity$.

We finally arrive at the Inventory $Q_t$ to maximise this control problem:

$Q_t approx = \frac{T-t}{T}Q_0$

Prerequisites:
  - Python 3.8+

References:
  - Almgren, Robert, and Neil Chriss. "Optimal execution of portfolio transactions." Journal of Risk 3 (2001): 5-40.
  - Donnelly, Ryan Francis, Optimal Execution: A Review (December 19, 2022). Available at SSRN: https://ssrn.com/abstract=4307177 or http://dx.doi.org/10.2139/ssrn.4307177.

Module:
  - Stochastic Control and Applications to Algorithmic Trading by Dr. Ryan Donnelly 




