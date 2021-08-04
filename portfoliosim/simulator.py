import pandas as pd
from .simulation import Simulation


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
        portfolio_allocation={
            'stocks' : 0.6,
            'bonds' : 0.4,
            'gold' : 0.0,
            'cash' : 0.0
            },
        cash_buffer_years=0,
        **simulation_cofig
        ):
        """
        creates simulator object that can run simulations

        Parameters:
            starting_portfolio_value: float, int
                Starting value of portfolio. Must be greater than 0
                Eg 100000

            desired_annual_income: float, int
                desired initial annual income. Must be greater than 0
                Eg 10000

            inflation: float
                annual inflation rate. Must be 0 or greater. Set to 1 for no inflation. Above 0 but less than 1
                indicates deflation
                Eg 1.02 (signifies 2% inflation)

            min_income_multiplier: float, default 0.5
                Multiplier signifying the minimum income relative to the desired income that one can accept
                Used when withdrawal rate would exceed max_withdrawal_rate. Min income is withdrawn instead
                Value should be between 0 and 1
                Eg 0.5 means that half of the desired annual income will be withdrawn when half the desired 
                income exceeds the withdrawal rate

            max_withdrawal_rate: float, default 0.02
                Maximum withdrawal rate before withdrawals get restricted. If desired withdrawal is more than
                max_withdrawal_rate, max_withdrawal_rate will be withdrawn instead
                should be a value between 0 and 1
                Eg 0.02 denotes a desired max withdrawal rate of 2%

            historical_data_source: file_path, default 'stock-data/us.csv'
                file path to historical income data csv
                data should contain 
                    year: year of this row of data (eg 1970)
                    month: month of this row of data (1-12)
                    gold: price of gold this month (relative to gold in other months)
                    stocks: price of stocks this month (relative to stocks in other months)
                    bonds: price of bonds this month (relative to bonds in other months)

            simulation_length_years: int. default 50
                length of the simulation in years
                must be greater than 0

            cash_buffer_years: int. default 0
                number of years of cash buffer to keep
                cash buffer is used to avoid drawing down from portfolio during downturns
            
            portfolio_allocation: dict, default {'stocks' : 0.6,'bonds' : 0.4,'gold' : 0.0,'cash' : 0.0}
                portfolio allocation among asset classes
            """
        # check validity of config data
        simulation_cofig['starting_portfolio_value']=starting_portfolio_value
        simulation_cofig['desired_annual_income']=desired_annual_income
        simulation_cofig['inflation']=inflation
        simulation_cofig['min_income_multiplier']=min_income_multiplier
        simulation_cofig['max_withdrawal_rate']=max_withdrawal_rate
        simulation_cofig['historical_data_source']=historical_data_source
        simulation_cofig['simulation_length_years']=simulation_length_years
        simulation_cofig['portfolio_allocation']=portfolio_allocation
        simulation_cofig['cash_buffer_years']=cash_buffer_years
        self.__check_config_validity(simulation_cofig)
        
        self.__simulation_config = simulation_cofig

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
                'starting_portfolio_value': starting_portfolio_value,
                'desired_annual_income': desired_annual_income,
                'inflation': inflation,
                'min_income_multiplier': min_income_multiplier,
                'max_withdrawal_rate': max_withdrawal_rate,
                }
        }

    def __check_config_validity(self,simulation_cofig):
        float_fields = ['desired_annual_income', 'inflation', 'min_income_multiplier','starting_portfolio_value','max_withdrawal_rate']
        int_fields = ['simulation_length_years']

        for i in float_fields:
            try:
                float(simulation_cofig[i])
            except ValueError:
                raise ValueError(f"{i} should be castable to float. received '{simulation_cofig[i]}' of type {type(simulation_cofig[i])}")
            

        for i in int_fields:
            try:
                int(simulation_cofig[i])
            except ValueError:
                raise ValueError(f"{i} should be castable to int. received '{simulation_cofig[i]}' of type {type(simulation_cofig[i])}")
        
        # check portfolio allocation values are castable to floats
        for key,value in simulation_cofig['portfolio_allocation'].items():
            try:
                float(value)
            except ValueError:
                raise ValueError(f"portfolio_allocation for {key} should be castable to float. received '{value}' of type {type(value)}")
        
        # check that portfolio asset classes are allowed types
        allowed_asset_classes = ('stocks','bonds','gold','cash')
        for key in simulation_cofig['portfolio_allocation']:
            if key not in allowed_asset_classes:
                raise TypeError(f"portfolio assets should only be stocks, bonds, cash, gold. received '{key}'")

        # check portfolio_allocation values are above at least zero
        for key,value in simulation_cofig['portfolio_allocation'].items():
            if float(value) < 0:
                raise ValueError(f"portfolio_allocation for {key} should be at least zero. received '{value}'")
        

        # check that certain inputs are above 0
        above_zero_fields = ['starting_portfolio_value','desired_annual_income','inflation','simulation_length_years']
        for i in above_zero_fields:
            if simulation_cofig[i] <= 0:
                raise ValueError( f"{i} should be greater than zero. received '{simulation_cofig[i]}'")

        # check that certain inputs are at least 0
        at_least_zero_fields = ['cash_buffer_years']
        for i in at_least_zero_fields:
            if simulation_cofig[i] < 0:
                raise ValueError( f"{i} should be at least zero. received '{simulation_cofig[i]}'")


        # check that certain inputs are between 0 and 1 inclusive
        between_zero_and_one_fields = ['min_income_multiplier']
        for i in between_zero_and_one_fields:
            if not (0 <= simulation_cofig[i] <= 1):
                raise ValueError(f"{i} should be between 0 and 1 inclusive. received '{simulation_cofig[i]}'")            

        # check that certain inputs are  positive and <=1
        positive_less_than_equal_to_one_fields = ['max_withdrawal_rate']
        for i in positive_less_than_equal_to_one_fields:
            if not (0 < simulation_cofig[i] <= 1):
                raise ValueError(f"{i} should be greater than zero and less than or equal to one. received '{simulation_cofig[i]}'")            
               

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
        wrapper to call run_simulations_wrapped
        """

        self.__run_simulations_wrapped(
            historical_data=self.__historical_data,
            income_schedule=self.__income_schedule,
            **self.__simulation_config
        )

    def __run_simulations_wrapped(
        self,
        starting_portfolio_value,
        max_withdrawal_rate,
        income_schedule,
        historical_data,
        simulation_length_years,
        portfolio_allocation,
        cash_buffer_years,
        **kwargs
        ):
        """
        Iteratively create and run simulations using different time frames

        Parameters:
            starting_portfolio_value: float, int
                Starting value of portfolio. Must be greater than 0
                Eg 100000

            income_schedule: dataframe
                data frame containing year on year values for desired and minimum income

            max_withdrawal_rate: float
                Maximum withdrawal rate before withdrawals get restricted. If desired withdrawal is more than
                max_withdrawal_rate, max_withdrawal_rate will be withdrawn instead
                should be a value between 0 and 1
                Eg 0.02 denotes a desired max withdrawal rate of 2%

            historical_data_source: data frame
                data frame containing historical asset prices
                data should contain 
                    year: year of this row of data (eg 1970)
                    month: month of this row of data (1-12)
                    gold: price of gold this month (relative to gold in other months)
                    stocks: price of stocks this month (relative to stocks in other months)
                    bonds: price of bonds this month (relative to bonds in other months)

            simulation_length_years: int
                length of the simulation in years
                must be greater than 0

            cash_buffer_years: int
                number of years of cash buffer to keep
                cash buffer is used to avoid drawing down from portfolio during downturns
            
            portfolio_allocation: dict
                portfolio allocation among asset classes
        """
        
        # get different time frames
        simulation_time_frames = self._generate_simulation_time_frames(historical_data,simulation_length_years)

        for historical_data_subset in simulation_time_frames:
            pass
            #       initialise simulation
            sim = Simulation(
                starting_portfolio_value,
                max_withdrawal_rate,
                income_schedule,
                historical_data_subset,
                portfolio_allocation,
                cash_buffer_years
                )
            #       run simulation
            #       extract simulation results and append to simulator results

        pass

    def _generate_simulation_time_frames(self,historical_data,simulation_length_years):
        """
        generate time frames to use for simulations

        Parameters:
            starting_portfolio_value: float, int
                Starting value of portfolio. Must be greater than 0
                Eg 100000

        Returns:
            time_frames: of time frames to run. Each list entry is a data frame containing 
            the time frame that should be run for a particular simulation. Each time frame contains 
            12 rows per year in  simulation_length_years
        """

        time_frames_list = []

        number_of_frames = len(historical_data) - (12 * simulation_length_years) + 1

        for i in range(number_of_frames):
            df = historical_data[i:(i+12*simulation_length_years)]
            df.reset_index(inplace=True,drop=True)
            time_frames_list.append(df)

        return(time_frames_list)

    def read_results(self):
        """
        returns results
        """
        pass
