import matplotlib.pyplot as plt
from src.filter_functions import *
import pandas as pd

def load_df_obd(filename):
    return pd.read_csv(filename, comment="#", skipinitialspace=True).drop_duplicates(subset=['Time (sec)'])

def col_to_array(df, y_col, x_col='Time (sec)'):
    x_array = df[x_col].to_numpy()
    y_array = df[y_col].to_numpy()

    return x_array, y_array

def plot_function(x, y, fun_list, arg_list, color="blue"):

    x_res, y_res = concat_funct(x, y, fun_list, arg_list)
    plt.plot(x_res, y_res, color= color)



if __name__ == "__main__":
    datafile = "CSVLog_20171014_181843.csv"
    column = "Engine RPM (RPM)"

    df = load_df_obd("src/testCsvData/" + datafile)
    x, y = col_to_array(df, column)

    #plot_function(x, y, [clipping_filter,interpolate_nan,moving_average,adaptive_smoothing_filter,peak_removal,resampling_nearest,resampling_linear], [[700 ,2500],[],[gauss_filter, 100],[20],[200],[x[::50]],[x[::50]]])

    plt.plot(x, y, "black")
    #plot_function(x, y, [clipping_filter, moving_average], [[700 ,2500], [gauss_filter, 200]], "cornflowerblue")
    #plot_function(x, y, [clipping_filter], [[700 ,2500]], "red")
    #plot_function(x, y, [interpolate_nan],[[]], "yellow")
    #plot_function(x, y, [moving_average], [[gauss_filter, 100]], "cyan")
    #plot_function(x, y, [moving_average], [[box_filter, 40]], "deepskyblue")
    #plot_function(x, y, [adaptive_smoothing_filter], [[20]], "orange")
    #plot_function(x, y, [adaptive_smoothing_filter], [[200]], "darkorange")
    #plot_function(x[::10], y[::10], [peak_removal], [[2000]], "lime")
    #plot_function(x, y, [filter_derivative_smoothing], [[box_filter, 100]], "navy")
    #plot_function(x, y, [resampling_nearest], [[x[::5]]], "mediumpurple")
    #plot_function(x, y, [resampling_nearest], [[x[::50]]], "mediumorchid")
    #plot_function(x, y, [resampling_linear], [[x[::5]]], "orchid")

    plt.show()
