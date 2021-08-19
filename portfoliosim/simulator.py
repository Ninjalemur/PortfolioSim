import pandas as pd
from .simulation import Simulation
import pathlib
import datetime
import time
import progressbar

class Simulator():
    """
    Simulator object that can spawn and run multiple simulations
    """
    def __init__(
        self,
        starting_portfolio_value,
        desired_annual_income=999999999,
        inflation=1,
        min_income_multiplier=1,
        max_withdrawal_rate=1.0,
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
                file path to historical income data csv, or data frame
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
        self.__simulator_id = self._generate_simulator_id()

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
        self.__simulator_inputs = {
            'simulator_id': self.__simulator_id,
            'starting_portfolio_value': starting_portfolio_value,
            'desired_annual_income': desired_annual_income,
            'inflation': inflation,
            'min_income_multiplier': min_income_multiplier,
            'max_withdrawal_rate': max_withdrawal_rate,
            'cash_buffer_years': cash_buffer_years,
            'portfolio_allocation': portfolio_allocation
            }
        
        self.__run_results = pd.DataFrame({
            'simulator_id':pd.Series([], dtype='int'),
            'run_id':pd.Series([], dtype='int'),
            'start_ref_year':pd.Series([], dtype='int'),
            'start_ref_month':pd.Series([], dtype='int'),
            'end_ref_year':pd.Series([], dtype='int'),
            'end_ref_month':pd.Series([], dtype='int'),
            'final_value':pd.Series([], dtype='float'), 
            'survival_duration':pd.Series([], dtype='int')
            })
        
        self.__timestep_data = pd.DataFrame({
            'simulator_id': self.__simulator_id,
            'run_id':pd.Series([], dtype='int'),
            'timestep':pd.Series([], dtype='int'),
            'year':pd.Series([], dtype='int'),
            'month':pd.Series([], dtype='int'),
            'cash_buffer':pd.Series([], dtype='float'),
            'bonds_qty':pd.Series([], dtype='float'),
            'stocks_qty':pd.Series([], dtype='float'),
            'gold_qty':pd.Series([], dtype='float'),
            'bonds_value':pd.Series([], dtype='float'),
            'stocks_value':pd.Series([], dtype='float'),
            'gold_value':pd.Series([], dtype='float'),
            'cash_notional':pd.Series([], dtype='float'),
            'allowance':pd.Series([], dtype='float'),
            'desired_allowance':pd.Series([], dtype='float'),
            'failed':pd.Series([], dtype='boolean')
            })

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
        if str(type(historical_data_source)) == "<class 'pandas.core.frame.DataFrame'>":
            historical_data = historical_data_source
        else:
            historical_data = pd.read_csv(historical_data_source)
            for column in historical_data.columns:
                if column not in ['year','month']:
                    historical_data[column] = pd.to_numeric(historical_data[column])
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
    def _generate_simulator_id(self):
        ct = datetime.datetime.now()
        ts = ct.timestamp()
        simulator_id = int(float(ts * 10**6))
        return(simulator_id)

    def _get_income_schedule(self):
        return(self.__income_schedule)
    def _get_run_results(self):
        return(self.__run_results)
    def _get_timestep_data(self):
        return(self.__timestep_data)
    def _get_simulator_inputs(self):
        return(self.__simulator_inputs)
    def _get_simulator_inputs_df(self):
        
        df = pd.DataFrame({
            'simulator_id':pd.Series([self.__simulator_inputs['simulator_id']], dtype='int64'),
            'starting_portfolio_value':pd.Series([self.__simulator_inputs['starting_portfolio_value']], dtype='float'),
            'desired_annual_income':pd.Series([self.__simulator_inputs['desired_annual_income']], dtype='float'),
            'inflation':pd.Series([self.__simulator_inputs['inflation']], dtype='float'),
            'min_income_multiplier':pd.Series([self.__simulator_inputs['min_income_multiplier']], dtype='float'),
            'max_withdrawal_rate':pd.Series([self.__simulator_inputs['max_withdrawal_rate']], dtype='float'),
            'cash_buffer_years':pd.Series([self.__simulator_inputs['cash_buffer_years']], dtype='int'),
            'stocks_allocation':pd.Series([self.__simulator_inputs['portfolio_allocation']['stocks']], dtype='float'),
            'bonds_allocation':pd.Series([self.__simulator_inputs['portfolio_allocation']['bonds']], dtype='float'),
            'gold_allocation':pd.Series([self.__simulator_inputs['portfolio_allocation']['gold']], dtype='float'),
            'cash_allocation':pd.Series([self.__simulator_inputs['portfolio_allocation']['cash']], dtype='float')
            })
        
        return(df)
    
    

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
        
        run_results_list = [] # for use in concatenating data frames later
        timestep_data_list = [] # for use in concatenating data frames later

        bar = progressbar.ProgressBar()
        for i in bar(range(len(simulation_time_frames))):
        # for i,historical_data_subset in enumerate(simulation_time_frames):
        #     if (i+1)%100 == 0:
        #         print(f'running simulation {i+1} of {len(simulation_time_frames)}')
            #       initialise simulation
            historical_data_subset = simulation_time_frames[i]
            sim = Simulation(
                starting_portfolio_value,
                max_withdrawal_rate,
                income_schedule,
                historical_data_subset,
                portfolio_allocation,
                cash_buffer_years
                )
            #       run simulation
            run_results, timestep_data = sim.run()
            
            #       extract simulation results and append to simulator results
            # self.__run_results = self.__run_results.append(run_results)
            # self.__timestep_data = self.__timestep_data.append(timestep_data)

            run_results_list.append(run_results)
            timestep_data_list.append(timestep_data)
        
        self.__run_results = pd.concat([self.__run_results]+run_results_list,axis=0,ignore_index=True)
        self.__timestep_data = pd.concat([self.__timestep_data]+timestep_data_list,axis=0,ignore_index=True)

        self.__run_results['simulator_id'] = self.__simulator_id
        self.__timestep_data['simulator_id'] = self.__simulator_id

       
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
            1 rows per year in  simulation_length_years. Other 11 months per year are not needed
        """

        time_frames_list = []

        number_of_frames = len(historical_data) - (12 * simulation_length_years) + 1

        for i in range(number_of_frames):
            df = historical_data[i:(i+12*simulation_length_years)]
            df = df[::12]
            df.reset_index(inplace=True,drop=True)
            time_frames_list.append(df)

        return(time_frames_list)

    def write_results(self,results_directory='./results/'):
        """
        writes results to folder
        """
        results_folder = results_directory+str(self.__simulator_id)+'/'
        path = pathlib.Path(results_folder)
        path.mkdir(parents=True, exist_ok=True)

        run_results = self._get_run_results()
        run_results.to_csv(results_folder+'run_results.csv',index=False)

        timestep_data = self._get_timestep_data()
        timestep_data.to_csv(results_folder+'timestep_data.csv',index=False)

        historical_data = self.__historical_data
        historical_data['simulator_id'] = self.__simulator_id
        historical_data.to_csv(results_folder+'historical_data.csv',index=False)

        simulation_inputs = self._get_simulator_inputs_df()
        simulation_inputs.to_csv(results_folder+'simulation_inputs.csv',index=False)


