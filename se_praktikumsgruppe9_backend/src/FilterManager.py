from typing import List, Dict
import pandas as pd
from filter_functions import *


class FilterManager:

    def __init__(self):
        functions = [clipping_filter,
                     interpolate_nan,
                     moving_average,
                     adaptive_smoothing_filter,
                     peak_removal,
                     filter_derivative_smoothing,
                     resampling_nearest,
                     resampling_linear]
        self.functions_dict = dict(zip(range(len(functions)), functions))

    def filterFunctions(self, x_y_values: pd.DataFrame, function_ids: list[int], args: list[list]) -> pd.DataFrame:
        functions = [self.functions_dict[function_id] for function_id in function_ids]

        x_array = x_y_values[x_y_values.keys()[0]]
        y_array = x_y_values[x_y_values.keys()[1]]


        filtered_x, filtered_y = concat_funct(x_array, y_array, functions, args)

        return pd.DataFrame({"X": filtered_x, "Y": filtered_y})
