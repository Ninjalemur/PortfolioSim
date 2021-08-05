import portfoliosim as ps
import pandas as pd


def test_simulator_run_get_timeframe():
    """
    Ensure that simulator correctly computes time frames when generating time frames
    
    first time frame should be starting from first time point in historical data
    each subsequent time frame slides forward one time point (ie one month)

    each time frame should contain time points exactly one year apart
    """
    simulation_cofig = {
        'starting_portfolio_value': 1000000.0,
        "desired_annual_income": 100000,
        "inflation": 1.01,
        "min_income_multiplier": 0.5,
        "max_withdrawal_rate" : 0.02,
        'simulation_length_years' : 50
        }

    x = ps.Simulator(**simulation_cofig)
    historical_data = pd.DataFrame(data={
        'year': 12*[2000]+12*[2001], 
        'month': 2*list(range(1,13)),
        'gold': 24*[1],
        'bonds': 24*[1],
        'stocks': 24*[1]
        })
    simulation_length_years=1

    time_frames = x._generate_simulation_time_frames(historical_data,simulation_length_years)
    first_time_frame = pd.DataFrame(data={
        'year': [2000], 
        'month': [1],
        'gold': [1],
        'bonds': [1],
        'stocks': [1]
        })
    last_time_frame = pd.DataFrame(data={
        'year': [2001], 
        'month': [1],
        'gold': [1],
        'bonds': [1],
        'stocks': [1]
        })
    number_time_frames = 13

    assert len(time_frames) == number_time_frames 
    pd.testing.assert_frame_equal(time_frames[0],first_time_frame)
    pd.testing.assert_frame_equal(time_frames[-1],last_time_frame)

   