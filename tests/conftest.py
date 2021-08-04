# import portfoliosim as ps
# import pandas as pd
# import pytest


# class TestingSimulator(ps.Simulator):
#     def set_historical_data(self,dataframe):
#         """
#         sets historical data to supplied dataframe
#         used for testing purposes
#         """
#         self.__historical_data = dataframe
    
#     def _get_historical_data(self):
#         return(self.__historical_data)

# @pytest.fixture
# def create_TestingSimulator():
#     return(TestingSimulator)