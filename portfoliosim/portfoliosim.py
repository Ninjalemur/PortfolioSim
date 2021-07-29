import pandas as pd

class Simulator():
    """
    Simulator object that can spawn and run multiple simulations
    """
    def __init__(self):
        # needs strategy function to pass to simulations
        # needs to load historical data for instruments
        # needs to load desired income schedule
        # initialise empty container to store results
        pass

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
