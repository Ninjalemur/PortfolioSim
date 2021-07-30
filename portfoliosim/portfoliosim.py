import pandas as pd


class Simulator():
    """
    Simulator object that can spawn and run multiple simulations
    """
    def __init__(self,income_data,historical_data_source='stock-data/us.csv',simulation_length_years=50):
        """
        creates simulator object that can run simulations

        args:
            income_data: dictionary containing desired_annual_income, inflation, min_income_multiplier
            historical_data_source: file path to historical income data csv


        returns:
            data frame of historical data
        """
        # needs strategy function to pass to simulations
        # needs to load historical data for instruments
        self.__historical_data = self.__load_historical_data(historical_data_source)

        # needs to load desired income schedule
        self.__income_schedule = self.__create_income_schedule(income_data,simulation_length_years)

        # initialise empty container to store results
        pass

    def __load_historical_data(self,historical_data_source):
        """
        loads historical data from file to simulator object

        args:
            historical_data_source: file path to historical income data csv

        returns:
            data frame of historical data
        """
        historical_data = pd.read_csv(historical_data_source)
        return(historical_data)

    def __create_income_schedule(self,income_data,simulation_length_years):
        """
        creates income schedule

        args:
            income_data: dictionary containing desired_annual_income, inflation, min_income_multiplier

        returns:
            income schedule: data frame containing year, desired_income, min_income
        """
        # check income data inputs
        for i in ['desired_annual_income', 'inflation', 'min_income_multiplier']:
            try:
                float(income_data[i])
            except ValueError:
                raise ValueError(f"{i} should be castable to float. received '{income_data[i]}' of type {type(income_data[i])}")

        income_schedule = pd.DataFrame({
            'year':pd.Series([], dtype='str'),
            'desired_income':pd.Series([], dtype='float'),
            'min_income':pd.Series([], dtype='float')
            })

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

