import pandas as pd

class Simulator():
    """
    Simulator object that can spawn and run multiple simulations
    """
    def __init__(self,historical_data_source='stock-data/us.csv'):
        # needs strategy function to pass to simulations
        # needs to load historical data for instruments
        self.historical_data = self.__load_historical_data(historical_data_source)
        # needs to load desired income schedule
        # initialise empty container to store results
        pass

    def __load_historical_data(self,historical_data_source):
        """
        loads historical data from file to simulator object

        args:
            historical_data_source: file path

        returns:
            data frame of historical data
        """
        historical_data = pd.read_csv(historical_data_source)
        return(historical_data)

    def run_simulations(self):
        """
        runs simulations one after another and collects results
        """
        pass

    def read_results(self):
        """
        returns results
        """
        pass

class Simulation():
    def __init__(self):
        """
        Simulation that simulates portfolio withdrawal over a time frame and records how well portfolio and strategy perform
        """
        # need to track portfolio allocation
        # need to have historical data reference
        # need desired income schedule
        # need empty container to store results
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

