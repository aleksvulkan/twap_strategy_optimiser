import dash
from dash import dcc, html, Input, Output, State
import plotly.graph_objects as go
import numpy as np
from twap_solver import TWAPSolver

app = dash.Dash(__name__)
server = app.server

app.layout = html.Div([
    html.H1("TWAP Strategy Optimizer"),

    html.Label("Number of Shares to Execute (Q):"),
    dcc.Input(id="input-q", type="number", value=1000),

    html.Label("Number of Time Steps (N):"),
    dcc.Input(id="input-n", type="number", value=10),

    html.Label("Gamma (Penalty for Fast Trading):"),
    dcc.Input(id="input-gamma", type="number", value=0.2, step=0.05),

    html.Label("Stock Ticker:"),
    dcc.Input(id="input-s", type="text", value="AAPL"),  # Fix here: type="text", default value is a string

    html.Button("Compute TWAP", id="compute-btn", n_clicks=0),

    dcc.Graph(id="execution-schedule"),
    dcc.Graph(id="cumulative-execution")
])


@app.callback(
    Output("execution-schedule", "figure"),
    Output("cumulative-execution", "figure"),
    Input("compute-btn", "n_clicks"),
    State("input-q", "value"),
    State("input-n", "value"),
    State("input-gamma", "value"),
    State("input-s", "value"),
)
def update_twap(n_clicks, q, n, gamma, ticker):
    if n_clicks == 0:
        return dash.no_update, dash.no_update  # Must return a tuple for multiple outputs

    solver = TWAPSolver(Q=q, N=n, gamma=gamma, ticker=ticker)
    actions = solver.solve()
    times = solver.get_execution_times()
    cum_exec = solver.get_cumulative_execution()

    fig1 = go.Figure()
    fig1.add_trace(go.Bar(x=times, y=actions, name="Order Size"))
    fig1.update_layout(title="Execution Schedule", xaxis_title="Time", yaxis_title="Shares")

    fig2 = go.Figure()
    fig2.add_trace(go.Scatter(x=times, y=cum_exec, mode="lines+markers", name="Cumulative Execution"))
    fig2.add_trace(go.Scatter(x=times, y=np.linspace(0, q, n), mode="lines", name="Ideal TWAP", line=dict(dash="dash")))
    fig2.update_layout(title="Cumulative Execution vs TWAP", xaxis_title="Time", yaxis_title="Cumulative Shares")

    return fig1, fig2


if __name__ == "__main__":
    app.run(debug=True)