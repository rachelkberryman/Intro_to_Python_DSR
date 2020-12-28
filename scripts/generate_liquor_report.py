import os
import argparse
import pandas as pd 

'''
Iowa Liquor Report Generation Script.
Written by User XX on 8 September, 2020. 

The purpose of this script is to automatically generate the monthly liquor sales 
KPIs required by the government. The data that is used is the general 
liquor sales CSV. 
The report is generated each month, for a given month and year.
A companion script called "liqour_data_checks.py" runs automatic data 
quality checks and should be run before reports are created with this script.
'''
print('Starting Report Generation')
def create_monthly_report(year, month):

    # loading the csv containing base data
    data = pd.read_csv('data/liquor/iowa_liquor_sales.csv', index_col=0)
    # converting date column's datatype
    data.loc[:, 'Date'] = pd.to_datetime(data.loc[:, 'Date'])

    # Test that the date column's type has been correctly changed
    assert str(data.loc[:, 'Date'].dtypes) == 'datetime64[ns]', "Check data type of 'Date' column"

    # selecting a subset of the data for the desired year and month
    month_data = data.loc[(data['Date'].dt.month==month) & (data['Date'].dt.year==year)]

    # Checking that the data only contains data from the correct subset
    assert all(month_data.loc[:, 'Date'].dt.month == month)
    assert all(month_data.loc[:, 'Date'].dt.year == year)

    # Further data cleaning needed for calculating the necessary KPIs
    # removing dollar signs so that columns can be converted to numeric
    month_data = month_data.replace('\$', '', regex=True)
    # removing commas in 1000s
    month_data = month_data.replace(',','', regex=True)

    # making list of columns to switch to numeric format
    columns_to_numeric = ['Sale (Dollars)', 'State Bottle Cost', 'State Bottle Retail']

    # converting each column in the list to numeric format
    for column in columns_to_numeric:
        month_data.loc[:, column] = pd.to_numeric(month_data.loc[:, column])

    # Starting to calculate KPIs

    # KPI 1: Store with most revenue
    # starting by grouping by stores. Using sum as the aggregator to get total sales/revenue
    stores_data_total = month_data.groupby('Store Name').sum()
    # finding store with highest total revenue, from Sale (Dollars) column
    highest_revenue_store = stores_data_total.loc[:, 'Sale (Dollars)'].idxmax()
    
    # looking at highest revenue store name
    highest_revenue_store

    # KPI 2: Average revenue across all of Iowa
    # Calculating average revenue 
    month_avg_revenue = month_data.loc[:, 'Sale (Dollars)'].mean()


    # KPI 3: Most sold item in the month
    # grouping data by item totals
    month_by_item = month_data.groupby('Item Description').sum()
    # Calculating average revenue 
    month_highest_sold_item = month_by_item.loc[:, 'Bottles Sold'].idxmax()


    # KPI 4: Total orders sold in the month
    # each row in the data represents one order, so counting rows to get number of orders
    month_orders = month_data.shape[0]


    # Generating Report txt file

    # Using month and year that were imported to initiate the file
    intro_line = '''IOWA STATE LIQUOR REPORT \n \n
    Report for {} {} \n \n
    '''.format(month, year)

    # adding each KPI and a small description about it to their own lines
    kpi1_line = 'KPI 1: \n Highest revenue store is : {} \n  \n'.format(highest_revenue_store)

    kpi2_line = 'KPI 2: \n Average monthly revenue is: {} \n  \n'.format(month_avg_revenue)

    kpi3_line = 'KPI 3: \n Most common item sold : {} \n  \n'.format(month_highest_sold_item)

    kpi4_line = 'KPI 4: \n Total orders : {} \n  \n'.format(month_orders)

    # combining all lines to be included in the report in a list to be added to the report file
    all_lines = [
        intro_line,
        kpi1_line,
        kpi2_line,
        kpi3_line,
        kpi4_line
    ]

    # checking if directory to save report in exists, if not, creating it
    if not os.path.exists('reports'):
        os.mkdir('reports')


    # opening the new file that we will write to 
    report_file = open("reports/report_{}_{}.txt".format(month, year),"w") 
    # writing all liens to it
    report_file.writelines(all_lines) 
    # closing file
    report_file.close()
    
    # printing report in-line
    for line in all_lines:
        print(line)

    # leaving function
    return 

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Report generator')
    parser.add_argument('--year', action='store', type=int)
    parser.add_argument('--month', action='store', type=int)
    results = parser.parse_args()
    month = results.month
    year = results.year
    create_monthly_report(year, month)