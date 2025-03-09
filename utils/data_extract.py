import pandas as pd
import smear_api.tools

def fetch_combined_data(variables, start_year, end_year, quality='ANY', averaging='1', avg_type='NONE'):
    """
    Fetch data for the specified variables from the SMEAR API over a range of years and combine into a single DataFrame.

    Args:
    variables (list): List of variables to fetch.
    start_year (int): The starting year for the data fetch.
    end_year (int): The ending year for the data fetch.
    quality (str): The quality of data to fetch. Default is 'ANY'.
    averaging (str): The averaging interval in minutes. Default is '1'.
    avg_type (str): The type of averaging. Default is 'NONE'.

    Returns:
    pd.DataFrame: Combined data for the specified range.
    """

    combined_data = pd.DataFrame()

    for year in range(start_year, end_year + 1, 2):

        start_date = f"{year}-01-01"     # Need to modify for the date
        end_date = f"{min(year + 1, end_year)}-12-31"

        data_segment = smear_api.tools.getData(variables, start=start_date, end=end_date, 
                                               quality=quality, averaging=averaging, avg_type=avg_type)
        
        if not isinstance(data_segment, pd.DataFrame):
            data_segment = pd.DataFrame(data_segment)
        
        if 'time' in data_segment.columns:
            data_segment['time'] = pd.to_datetime(data_segment['time'])
            data_segment.set_index('time', inplace=True)

        combined_data = pd.concat([combined_data, data_segment])

    # Sort the combined data by the index (time) to maintain chronological order
    combined_data.sort_index(inplace=True)

    return combined_data