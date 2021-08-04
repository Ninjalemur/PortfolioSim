import pandas as pd

class Simulation():
    def __init__(
        self,
        starting_portfolio_value,
        max_withdrawal_rate,
        income_schedule,
        historical_data_subset,
        portfolio_allocation
        ):
        """
        Simulation that simulates portfolio withdrawal over a time frame and records how well portfolio and strategy perform
        """
        # allocate portfolio
        # self.

        self.__historical_data_subset =  historical_data_subset
        self.__income_schedule = income_schedule
        self.__max_withdrawal_rate = max_withdrawal_rate

        # need empty container to store results
        run_timestep_data = pd.DataFrame({
            'year':pd.Series([], dtype='int'),
            'cash_buffer':pd.Series([], dtype='float'),
            'bonds_qty':pd.Series([], dtype='float'),
            'stocks_qty':pd.Series([], dtype='float'),
            'gold_qty':pd.Series([], dtype='float'),
            'bonds_value':pd.Series([], dtype='float'),
            'stocks_value':pd.Series([], dtype='float'),
            'gold_value':pd.Series([], dtype='float'),
            'cash_value':pd.Series([], dtype='float'),
            'withdrawal':pd.Series([], dtype='float'),
            })
        pass

    def run(self):
        """
        runs simulation
        """
        pass

    def run_timestep(self):
        """
        runs a single time step of the simulation

        instrument prices update first, then strategy is executed
        """
        self.update_prices()
        self.execute_strategy()
        self.log_results()
    
    def update_prices(self):
        """
        update prices based on the current date
        """
        pass

    def execute_strategy(self):
        """
        executes strategy.
        rebalancing and withdrawals happen here
        """
        pass

    def log_results(self):
        """
        logs results to container
        """
        pass
