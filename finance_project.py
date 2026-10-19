import numpy as np
from matplotlib import pyplot as plt
import pandas as pd
#csv format: GS, HAS, LMT, NVDA, SPY

"""
These are the functions to read/clean the data and get the stock prices for each stock
"""
def read_csv(file_path):
    """
    Reads a CSV file and returns the data as a Numpy array.
    The first entry in the array is the date, then GS, HAS, LMT, NVDA, SPY
    """
    data = np.genfromtxt(file_path, delimiter=',', skip_header=1)
    return data

def get_stock(data):
    """
    returns a numpy array of the stock prices for GS, HAS, LMT, NVDA, SPY
    """
    return data[:, 1:6]

#be carefull of an indexing error when comparing this to retruns, we start returns from index 1
def get_stock_prices(data, stock_index):
    """
    returns a numpy array of the stock prices for a specific stock
    stock_index: 0 for GS, 1 for HAS, 2 for LMT, 3 for NVDA, 4 for SPY
    """
    return data[:, stock_index + 1]

#hypothetically this works, realistically need to write some unit tests
#thatll be a fun use of agents!

"""
These are the returns functions
"""
def find_returns(data):
    """
    returns the daily percentage returns for a given stock
    assumes data is a 1D array of stock prices for one specific stock
    """
    return_array = np.array([])
    for i in range(1, data.shape[0]):
        #will want to cover the NaN case here, but for now just assume no NaNs
        diff = data[i] - data[i-1]
        percente_change = diff / data[i-1]
        return_array = np.append(return_array, percente_change)
    return return_array

def log_returns(data):
    """
    returns the daily log returns for a given stock
    assumes data is a 1D array of stock prices for one specific stock
    """
    return_array = np.array([])
    for i in range(1, data.shape[0]):
        #will want to cover the NaN case here, but for now just assume no NaNs
        log_return = np.log(data[i] / data[i-1])
        return_array = np.append(return_array, log_return)
    return return_array

def mean_returns(data):
    """
    returns the mean daily returns for a given stock
    assumes data is a 1D array of stock prices for one specific stock
    """
    return np.mean(data)

def build_matrix(data1, data2, data3, data4, data5):
    matrix = np.array([data1, data2, data3, data4, data5])
    return matrix.T  # Transpose to have stocks as columns and returns as rows


#note, i think we need to use the covariance matrix with our orignal (trimmed) data
#but we can try it with the returns data as well
def covariance_matrix(matrix):
    """
    returns the covariance matrix for the given stock data
    assumes data is a 2D array of returns for multiple stocks
    """
    return np.cov(matrix, rowvar=False)

#next, we want to find the weights for a portfolio consisting of these stocks. 
"""
these are the functions for deciding weights for the portfolio."""
def global_minimum_variance_portfolio(cov_matrix, mean_data, risk_free_rate):
    """
    returns the weights for the global minimum variance portfolio
    assumes cov_matrix is a 2D array of the covariance matrix for multiple stocks
    """
    inv_cov_matrix = np.linalg.inv(cov_matrix)
    ones = np.ones(inv_cov_matrix.shape[0])
    m = np.array(mean_data)
    weights = ((m - risk_free_rate * ones) @ inv_cov_matrix) / ((m - risk_free_rate * ones) @ inv_cov_matrix @ones.T)
    return weights

# we gotta fix the market portfolio function

def set_rate_portfolio(cov_matrix, mean_data):
    """
    returns the weights for the portfolio that sets the rate of return to the risk-free rate
    assumes cov_matrix is a 2D array of the covariance matrix for multiple stocks
    """
    inv_cov_matrix = np.linalg.inv(cov_matrix)
    ones = np.ones(inv_cov_matrix.shape[0])
    m = np.array(mean_data)
    weights = ((m - 0.04 * ones) @ inv_cov_matrix) / ((m - 0.04 * ones) @ inv_cov_matrix @ ones.T)
    return weights

def diversified_portfolio(cov_matrix, mean_data):
    """
    returns the weights for the diversified portfolio, assuming risk-free rate is 0
    assumes cov_matrix is a 2D array of the covariance matrix for multiple stocks
    """
    inv_cov_matrix = np.linalg.inv(cov_matrix)
    ones = np.ones(inv_cov_matrix.shape[0])
    m = np.array(mean_data)
    weights = (m  @ inv_cov_matrix) / (m @ inv_cov_matrix @ones.T)
    return weights

def build_portfolio(weights_array, stock_array):
    """
    simulates a portfolio with each stock wieghted by the given weights
    assumes weights_array is a 1D array of weights for each stock
    assumes stock_array is a 2D array of stock prices for multiple stocks
    rerturns a 1D array of the portfolio value for each day
    """
    return np.dot(stock_array, weights_array)



#these are all the graphic functions
def scatter_plot(data, xlabel, ylabel, fig_title):
    """
    returns a scatter plot of the returns for the given stock data
    Assumes the x-axis is days, and y axis is retruns.
    """
    plt.scatter(range(data.shape[0]), data)
    plt.xlabel(f"{xlabel}")
    plt.ylabel(f"{ylabel}")
    plt.title(f"{fig_title}")
    plt.savefig(f"/home/charlie-godfrey/code/python/.venv/Finance project/{fig_title}.png")

def line_plot(data, xlabel, ylabel, fig_title):
    """
    returns a line plot for the given stock data
    Assumes the x-axis is days, and y axis is the data.
    """
    plt.plot(range(data.shape[0]), data)
    plt.xlabel(f"{xlabel}")
    plt.ylabel(f"{ylabel}")
    plt.title(f"{fig_title}")
    plt.savefig(f"/home/charlie-godfrey/code/python/.venv/Finance project/{fig_title}.png")

#this is going to be way to long, maybe we just put a truncated example?
def table_plot(data_matrix, fig_title):
    """
    returns a table plot for the given stock data
    Assumes the x-axis is days, and y axis is the data.
    """
    nrows = len(data_matrix)
    fig_height = max(3, nrows * 0.35)
    fig, ax = plt.subplots(figsize=(10, fig_height))
    ax.axis('tight')
    ax.axis('off')
    table = ax.table(cellText=data_matrix, colLabels=["GS", "HAS", "LMT", "NVDA", "SPY"], loc='center')
    table.auto_set_font_size(False)
    table.set_fontsize(10)
    table.scale(1.0, 1.5)
    plt.title(f"{fig_title}")
    plt.savefig(f"/home/charlie-godfrey/code/python/.venv/Finance project/{fig_title}.png")

# this is just a checker for weights adding up to one
def weight_check(weights_array):
    """
    checks if the weights add up to 1
    assumes weights_array is a 1D array of weights for each stock
    """
    return np.sum(weights_array) == 1.0, np.sum(weights_array)


#we will probably want a Sharpe ratio function to compare our portfolios against


#reading the file and getting the stock prices for each stock
data = read_csv("/home/charlie-godfrey/code/python/.venv/Finance project/finance_data.csv")
stock_data = get_stock(data)
gs_prices = get_stock_prices(data, 0)
has_prices = get_stock_prices(data, 1)
lmt_prices = get_stock_prices(data, 2)
nvda_prices = get_stock_prices(data, 3)
spy_prices = get_stock_prices(data, 4)  

#percentage retrun data
gs_returns = find_returns(get_stock_prices(data, 0))
has_returns = find_returns(get_stock_prices(data, 1))
lmt_returns = find_returns(get_stock_prices(data, 2))
nvda_returns = find_returns(get_stock_prices(data, 3))
spy_returns = find_returns(get_stock_prices(data, 4))

#log retrun data
gs_ln_returns = log_returns(get_stock_prices(data, 0))
has_ln_returns = log_returns(get_stock_prices(data, 1))
lmt_ln_returns = log_returns(get_stock_prices(data, 2))
nvda_ln_returns = log_returns(get_stock_prices(data, 3))
spy_ln_returns = log_returns(get_stock_prices(data, 4))

#mean return data
gs_mean_return = mean_returns(gs_returns)
has_mean_return = mean_returns(has_returns)
lmt_mean_return = mean_returns(lmt_returns)
nvda_mean_return = mean_returns(nvda_returns)
spy_mean_return = mean_returns(spy_returns)



price_matrix = build_matrix(gs_prices, has_prices, lmt_prices, nvda_prices, spy_prices)
percentage_returns = build_matrix(gs_returns, has_returns, lmt_returns, nvda_returns, spy_returns)
ln_returns = build_matrix(gs_ln_returns, has_ln_returns, lmt_ln_returns, nvda_ln_returns, spy_ln_returns)

#the covariance matrices for the price and return data
cov_matrix_price = covariance_matrix(price_matrix)
cov_matrix_returns = covariance_matrix(percentage_returns)

mean_array = np.array([gs_mean_return, has_mean_return, lmt_mean_return, nvda_mean_return, spy_mean_return])

#using the price covariance matrix
set_rate_portfolio_weights_prices = set_rate_portfolio(cov_matrix_price, mean_array)
diversified_portfolio_weights_prices = diversified_portfolio(cov_matrix_price, mean_array)

#using the returns covariance matrix
set_rate_portfolio_weights_returns = set_rate_portfolio(cov_matrix_returns, mean_array)
diversified_portfolio_weights_returns = diversified_portfolio(cov_matrix_returns, mean_array)

#somethings wrong, we're getting negative average returns. either in the weights or in the portfolio simulation. need to check the math and the data.
set_rate_portfolio_prices = build_portfolio(set_rate_portfolio_weights_prices, price_matrix)
diversified_portfolio_prices = build_portfolio(diversified_portfolio_weights_prices, price_matrix)

#try with return covariance matrix
set_rate_portfolio_returns = build_portfolio(set_rate_portfolio_weights_returns, price_matrix)
diversified_portfolio_returns = build_portfolio(diversified_portfolio_weights_returns, price_matrix)


#these are the checks for the weights adding up to 1
set_rate_Prices_weights_check = weight_check(set_rate_portfolio_weights_prices)
diversified_prices_weights_check = weight_check(diversified_portfolio_weights_prices)
set_rate_returns_weights_check = weight_check(set_rate_portfolio_weights_returns)
diversified_returns_weights_check = weight_check(diversified_portfolio_weights_returns)


print(f"Set Rate Portfolio Weights: {set_rate_portfolio_weights_prices} Passes Check: {set_rate_Prices_weights_check}")
print(f"Diversified Portfolio Weights: {diversified_portfolio_weights_prices} Passes Check: {diversified_prices_weights_check}")
print(f"Set Rate Portfolio Weights (Returns): {set_rate_portfolio_weights_returns} Passes Check: {set_rate_returns_weights_check}")
print(f"Diversified Portfolio Weights (Returns): {diversified_portfolio_weights_returns} Passes Check: {diversified_returns_weights_check}")



"""
These are all the plots for the individual stock prices, returns, and log returns.
"""
#line plots for the individual stock prices

#line_plot(gs_prices, "Days", "GS Prices", "GS Prices")
#line_plot(has_prices, "Days", "HAS Prices", "HAS Prices")
#line_plot(lmt_prices, "Days", "LMT Prices", "LMT Prices")
#line_plot(nvda_prices, "Days", "NVDA Prices", "NVDA Prices")
#line_plot(spy_prices, "Days", "SPY Prices", "SPY Prices")

#scatter plots for the individual stock returns

#scatter_plot(gs_returns, "Days", "GS Returns", "GS Returns")
#scatter_plot(has_returns, "Days", "HAS Returns", "HAS Returns")
#scatter_plot(lmt_returns, "Days", "LMT Returns", "LMT Returns")
#scatter_plot(nvda_returns, "Days", "NVDA Returns", "NVDA Returns")
#scatter_plot(spy_returns, "Days", "SPY Returns", "SPY Returns")

#scatter plots for the individual stock log returns
#scatter_plot(gs_ln_returns, "Days", "GS Log Returns", "GS Log Returns")
#scatter_plot(has_ln_returns, "Days", "HAS Log Returns", "HAS Log Returns")
#scatter_plot(lmt_ln_returns, "Days", "LMT Log Returns", "LMT Log Returns")
#scatter_plot(nvda_ln_returns, "Days", "NVDA Log Returns", "NVDA Log Returns")
#scatter_plot(spy_ln_returns, "Days", "SPY Log Returns", "SPY Log Returns")

