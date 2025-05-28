import numpy as np
import yfinance as yf

class TWAPSolver:
    def __init__(self, Q: int, N: int, T: float = 1.0, gamma: float = 0.1, ticker: str = "AAPL"):
        """
        Initialize TWAP solver with live price feed.

        Parameters:
        Q: Total quantity to sell
        N: Number of discrete time steps
        T: Total time horizon (e.g., 1.0 for 1 day)
        gamma: Market impact penalty coefficient
        ticker: Stock ticker symbol to fetch live prices
        """
        self.Q = Q
        self.N = N
        self.T = T
        self.dt = T / N
        self.gamma = gamma
        self.ticker = ticker
        self.S_k = self.fetch_live_prices()
        self.V = np.full((N + 1, Q + 1), np.inf)
        self.V[N, 0] = 0  # Terminal condition
        self.actions = []

    def fetch_live_prices(self):
        """
        Fetch recent live prices using yfinance.
        Returns an array of length N.
        """
        try:
            stock = yf.Ticker(self.ticker)
            history = stock.history(period="1d", interval="1m")
            prices = history['Close'].dropna().values[-self.N:]
            if len(prices) < self.N:
                raise ValueError("Not enough price data.")
            return prices
        except Exception as e:
            print(f"Error fetching live prices for {self.ticker}: {e}")
            return np.ones(self.N) * 100  # fallback to constant price

    def solve(self):
        """
        Run dynamic programming to compute optimal execution strategy.
        """
        for k in reversed(range(self.N)):
            for q in range(self.Q + 1):
                for x in range(q + 1):
                    cost = self.S_k[k] * x + 0.5 * self.gamma * x ** 2
                    self.V[k, q] = min(self.V[k, q], cost + self.V[k + 1, q - x])

        # Recover optimal actions
        q = self.Q
        for k in range(self.N):
            best_x = 0
            best_val = np.inf
            for x in range(q + 1):
                cost = self.S_k[k] * x + 0.5 * self.gamma * x ** 2 + self.V[k + 1, q - x]
                if cost < best_val:
                    best_val = cost
                    best_x = x
            self.actions.append(best_x)
            q -= best_x

        return self.actions

    def get_cumulative_execution(self):
        return np.cumsum(self.actions)

    def get_execution_times(self):
        return np.linspace(0, self.T, self.N, endpoint=False)


if __name__ == "__main__":
    solver = TWAPSolver(Q=1000, N=10, gamma=0.2, ticker="AAPL")
    actions = solver.solve()
    print("Optimal execution schedule (shares per step):", actions)
    print("Cumulative execution:", solver.get_cumulative_execution())