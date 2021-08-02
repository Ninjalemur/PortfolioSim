import pandas as pd


class Simulator():
    """
    Simulator object that can spawn and run multiple simulations
    """
    def __init__(
        self,
        starting_portfolio_value,
        desired_annual_income,
        inflation,
        min_income_multiplier=0.5,
        max_withdrawal_rate=0.02,
        historical_data_source='stock-data/us.csv',
        simulation_length_years=50,
        **simulation_cofig
        ):
        """
        creates simulator object that can run simulations

        args:
            income_data: dictionary containing desired_annual_income, inflation, min_income_multiplier
            historical_data_source: file path to historical income data csv


        returns:
            data frame of historical data
        """
        # check validity of config data
        simulation_cofig['starting_portfolio_value']=starting_portfolio_value
        simulation_cofig['desired_annual_income']=desired_annual_income
        simulation_cofig['inflation']=inflation
        simulation_cofig['min_income_multiplier']=min_income_multiplier
        simulation_cofig['max_withdrawal_rate']=max_withdrawal_rate
        simulation_cofig['historical_data_source']=historical_data_source
        simulation_cofig['simulation_length_years']=simulation_length_years
        self.__check_config_validity(simulation_cofig)
        

        # needs strategy function to pass to simulations

        # needs to load historical data for instruments
        self.__historical_data = self.__load_historical_data(historical_data_source)

        # needs to load desired income schedule
        self.__income_schedule = self.__create_income_schedule(
            desired_annual_income,
            inflation,
            min_income_multiplier,
            simulation_length_years)

        # initialise empty data container to store results
        self.__results = {
            'simulator inputs': {
                'starting_portfolio_value': simulation_cofig['starting_portfolio_value'],
                'desired_annual_income': simulation_cofig['desired_annual_income'],
                'inflation': simulation_cofig['inflation'],
                'min_income_multiplier': simulation_cofig['min_income_multiplier'],
                'max_withdrawal_rate': simulation_cofig['max_withdrawal_rate'],
                }
        }

    def __check_config_validity(self,simulation_cofig):
        mandatory_fields=['desired_annual_income', 'inflation','starting_portfolio_value']
        float_fields = ['desired_annual_income', 'inflation', 'min_income_multiplier','starting_portfolio_value','max_withdrawal_rate'],
        int_fields = ['simulation_length_years']
        for i in float_fields:
            try:
                float(simulation_cofig[i])
            except ValueError:
                raise ValueError(f"{i} should be castable to float. received '{simulation_cofig[i]}' of type {type(simulation_cofig[i])}")
            except KeyError:
                pass

        for i in int_fields:
            try:
                int(simulation_cofig[i])
            except ValueError:
                raise ValueError(f"{i} should be castable to int. received '{simulation_cofig[i]}' of type {type(simulation_cofig[i])}")
            except KeyError:
                pass
        ### mandatory field check

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

    def __create_income_schedule(
        self,
        desired_annual_income,
        inflation,
        min_income_multiplier,
        simulation_length_years):
        """
        creates income schedule

        args:
            simulation_cofig: dictionary containing desired_annual_income, inflation, min_income_multiplier

        returns:
            income schedule: data frame containing year, desired_income, min_income
        """

        income_schedule = pd.DataFrame({
            'year':pd.Series([], dtype='int'),
            'desired_income':pd.Series([], dtype='float'),
            'min_income':pd.Series([], dtype='float')
            })
        

        for i in range(simulation_length_years):
            income_schedule = income_schedule.append(pd.DataFrame({
                'year':pd.Series([i+1], dtype='int'),
                'desired_income':pd.Series(
                    [desired_annual_income*(inflation**i)], 
                    dtype='float'
                    ),
                'min_income':pd.Series(
                    [min_income_multiplier*desired_annual_income*(inflation**i)], 
                    dtype='float'
                    )
                }))
        income_schedule.reset_index(drop=True, inplace=True)
        return(income_schedule)

    def _get_income_schedule(self):
        return(self.__income_schedule)

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

