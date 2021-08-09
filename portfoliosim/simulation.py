import pandas as pd

class Simulation():
    def __init__(
        self,
        starting_portfolio_value,
        max_withdrawal_rate,
        income_schedule,
        historical_data_subset,
        portfolio_allocation,
        cash_buffer_years
        ):
        """
        Simulation that simulates portfolio withdrawal over a time frame and records how well portfolio and strategy perform
        
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
        # create empty container to store results
        run_timestep_data = pd.DataFrame({
            'year':pd.Series([], dtype='int'),
            'cash_buffer':pd.Series([], dtype='float'),
            'bonds_qty':pd.Series([], dtype='float'),
            'stocks_qty':pd.Series([], dtype='float'),
            'gold_qty':pd.Series([], dtype='float'),
            'bonds_value':pd.Series([], dtype='float'),
            'stocks_value':pd.Series([], dtype='float'),
            'gold_value':pd.Series([], dtype='float'),
            'cash_notional':pd.Series([], dtype='float'),
            'withdrawal':pd.Series([], dtype='float'),
            })

        # normalise portfolio_allocation so that they total up to 1
        portfolio_allocation = self.__normalise_portfolio_allocation(portfolio_allocation)
    
        # store information
        self.__historical_data_subset =  historical_data_subset
        self.__income_schedule = income_schedule
        self.__max_withdrawal_rate = max_withdrawal_rate
        self.__income_schedule = income_schedule
        self.__portfolio_allocation = portfolio_allocation
        self.__cash_buffer_years = cash_buffer_years
        self.__allowance = 0
        
        self.__initialise_portfolio_cash_buffer(
            starting_portfolio_value,
            portfolio_allocation,
            cash_buffer_years,
            income_schedule,
            historical_data_subset
            )

    def __normalise_portfolio_allocation(self,portfolio_allocation):
        """
        normalises portfolio allocation to sum to 1
        """
        base = sum(portfolio_allocation.values())       
        for asset,allocation in portfolio_allocation.items():
            portfolio_allocation[asset] = allocation/base
        
        return(portfolio_allocation)

    def __initialise_portfolio_cash_buffer(
        self,
        starting_portfolio_value,
        portfolio_allocation,
        cash_buffer_years,
        income_schedule,
        historical_data_subset
        ):
        """
        creates initial portfolio and cash buffer before simulation runs

        portfolio only tracks holdings for gold, stocks, bonds, as these will fluctuate in value
        cash is tracked in notional amount

        cash buffer is a separate pool of cash not in the portfolio itself
        """
        self.__initialise_cash_buffer(
            starting_portfolio_value,
            income_schedule,
            cash_buffer_years
            )
        
        # subtract cash buffer from portfolio value, then allocation among asset classes
        self.__initialise_portfolio(
            starting_portfolio_value,
            portfolio_allocation,
            historical_data_subset
            )
        

    def get_portfolio(self):
        return(self.__portfolio)

    def get_cash_buffer(self):
        return(self.__cash_buffer)

    def get_current_prices(self):
        return(self.__current_prices)

    def get_max_withdrawal_rate(self):
        return(self.__max_withdrawal_rate)

    def __initialise_cash_buffer(
        self,
        starting_portfolio_value,
        income_schedule,
        cash_buffer_years
        ):
        """
        sets initial cash buffer at start of simulation
        """
        desired_cash_buffer = self.__get_desired_cash_buffer(
            income_schedule,
            cash_buffer_years,
            1)
        
        if desired_cash_buffer <= starting_portfolio_value:
            self.__cash_buffer=desired_cash_buffer
        else:
            self.__cash_buffer=starting_portfolio_value

    def __get_desired_cash_buffer(
        self,
        income_schedule,
        cash_buffer_years,
        current_year
        ):
        """
        Compute and return the desired cash buffer. Note that cash buffer
        holds desired income from NEXT year onwards

        Parameters:
            income_schedule: Data Frame
                data frame containing year, desired income, min_income
            
            cash_buffer_years: int
                number of years of desired income that should be held in cash buffer

            current_year: int
                current year in the simulation
        """
        desired_cash_buffer = income_schedule['desired_income'][current_year:current_year+cash_buffer_years].sum()
        return(desired_cash_buffer)

    def __initialise_portfolio(
        self,
        starting_portfolio_value,
        portfolio_allocation,
        historical_data_subset
        ):
        # get allocatable value for portfolio
        if self.get_cash_buffer() >= starting_portfolio_value:
            allocatable_value = 0
        else:
            allocatable_value = starting_portfolio_value - self.get_cash_buffer()

        # set portfolio to all cash initially
        self.__portfolio = {
            'stocks' : 0.0,
            'gold' : 0.0,
            'bonds' : 0.0,
            'cash' : float(allocatable_value)
            }

        # allocate portfolio
        self.allocate_portfolio(portfolio_allocation,historical_data_subset.iloc[0])

        # set initial prices
        self.update_prices(0)

    def allocate_portfolio(self,portfolio_allocation,current_prices):
        """
        allocate portfolio based on desired allocation and current prices
        """

        value_to_allocate = sum(self.__portfolio.values())

        for asset,value in self.__portfolio.items():
            asset_price = current_prices.get(asset,1)
            allocation_proportion = portfolio_allocation[asset]
            self.__portfolio[asset] = value_to_allocate * allocation_proportion / asset_price

    def run(self):
        """
        runs simulation
        """
        for i in range(len(self.__income_schedule)):
            self._run_timestep(i)

    def _run_timestep(self,timestep_number):
        """
        runs a single time step of the simulation

        instrument prices update first, then strategy is executed
        """
        self.__allowance = 0
        self.update_prices(timestep_number)
        self.execute_strategy(timestep_number)
        self.log_results()
    
    def update_prices(self,timestep_number):
        """
        update prices based on the current timestep
        """
        self.__current_prices = self.__historical_data_subset.iloc[timestep_number]
        pass

    def execute_strategy(self,timestep_number):
        """
        executes strategy.
        rebalancing and withdrawals happen here
        """

        desired_allowance = self._get_desired_allowance(timestep_number)
        min_income = self._get_min_income(timestep_number)
        withdrawal_limit = self._get_withdrawal_limit()
        
        pass

    def _get_desired_allowance(self,timestep):
        """
        get desired_allowance for a specific timestep

        Parameters:
            timestep: int
                timestep to retrieve desired_allowance for

        Returns:
            desired_allowance: float
                desired_allowance for this year of the simulation
        """

        return(self.__income_schedule.iloc[timestep]['desired_income'])

    def _get_min_income(self,timestep):
        """
        get min_income for a specific timestep

        Parameters:
            timestep: int
                timestep to retrieve min_income for

        Returns:
            min_income: float
                min_income for this year of the simulation
        """

        return(self.__income_schedule.iloc[timestep]['min_income'])
    
    def _get_withdrawal_limit(self):
        """
        get withdrawal limit at current point in time based on
        portfolio value and max_withdrawal_rate

        Returns:
            withdrawal_limit: float
                withdrawal limit at current point in time
        """
        return(self.get_max_withdrawal_rate() * sum(self.get_portfolio().values()))

    def _check_desired_less_than_max_withdrawal(self,desired_allowance,withdrawal_limit):
        """
        checks if desired allowance is less than max withdarwal limit
        returns True if yes, False if No
        """
        return(desired_allowance <= withdrawal_limit)

    def _check_remaining_withdrawal_amount_can_refill_buffer(self,desired_buffer,current_buffer,withdrawal_limit,consumed_withdrawal):
        """
        checks if withdrawal amount after allowance withdrawal enough to fill empty buffer
        returns True if yes, False if No
        """
        return(desired_buffer - current_buffer <= withdrawal_limit - consumed_withdrawal)

    def __top_up_cash_buffer_from_portfolio(self,amount):
        """
        top up cash buffer from portfolio
        """
        # subtract amount from portfolio cash portion
        # add amount to cash buffer
        self.__portfolio -= amount
        self.__cash_buffer += amount
    
    def _withdraw_allowance_from_portfolio(self,amount):
        """
        withdraw money from portfolio and add to allowance
        """
        # subtract amount from portfolio cash portion
        # add amount to allowance
        pass

    def _withdraw_allowance_from_cash_buffer(self,amount):
        """
        withdraw money from cash buffer and add to allowance
        """
        # subtract amount from cash_buffer
        # add amount to allowance
        pass

    def _check_cash_buffer_enough_funds_for_allowance(self,cash_buffer,desired_allowance):
        """
        check if cash buffer has enough funds for desired income
        return True if yes, False if no
        """
        pass

    def _check_max_withdrawal_allow_top_up_to_target_income(self,withdrawal_limit,target_allowance,current_allowance):
        """
        check if max withdrawal amount has sufficient value to top up current allowance to desired/minimum allowance
        return True if yes, False if no
        """
        pass



    def log_results(self):
        """
        logs results to container
        """
        pass
