import math
from typing import Tuple

import numpy as np
from numpy import ndarray
from scipy.signal import find_peaks


def concat_funct(x_array: ndarray, values: ndarray, functions, params) -> Tuple[ndarray, ndarray]:
    """
    Applies the given filter functions with their params iteratively onto the data points

    :param x_array: array_like, the x-coords

    :param values: array_like, the y-coords

    :param functions: list of functions to be applied onto the data

    :param params: list of params for each filter function

    :raises ValueError if x_array.size and values.size doesn't match
    :raises ValueError if x_array or values are empty
    :raises ValueError if no functions are given
    :raises ValueError if lenFgth of functions and length of parameter lists do not math
    :raises ValueError if items in x_array are not in ascending order
    :raises ValueError if x_array contains duplicates

    :return: x_array and new y_array, that contains the filtered data points
    """

    if x_array.size != values.size:
        raise ValueError("Anzahl x- und y-Werte stimmt nicht überein")

    if values.size == 0:
        raise ValueError("Keine Punkte zum Filtern übergeben")

    if len(functions) == 0:
        raise ValueError("Keine Funktion übergeben")

    if len(functions) != len(params):
        raise ValueError("Anzahl übergebener Funktionen stimmt nicht mit Anzahl übergebener Parameter überein")

    if np.any(np.diff(x_array) <= 0):
        raise ValueError("x-Werte sind nicht aufsteigend sortiert")

    if np.unique(x_array).size != np.size(x_array):
        raise ValueError("x-Werte sind nicht distinct")

    for i in range(len(functions)):
        try:
            x_array, values = functions[i](x_array, values, *params[i])
        except Exception as err:
            raise Exception("Fehler in folgender Funktion: " + functions[i].__name__ + ": " + err.args.__str__())

    return x_array, values


# FILTER 1
def clipping_filter(x_array: ndarray, values: ndarray, min_value: float, max_value: float) -> Tuple[ndarray, ndarray]:
    """
    Clip (limit) the values in an array.

    :param x_array: array_like, the x-coords
    :param values: array_like, the y-coords
    :param min_value: min border
    :param max_value: max border
    :raise ValueError: if min_value > max_value
    :return: Values outside the interval are clipped to the interval borders.
    """
    if min_value > max_value:
        raise ValueError("The given max value can't be smaller than the min value")

    return x_array, np.clip(values, min_value, max_value)


# FILTER 2
def interpolate_nan(x_array: ndarray, values: ndarray, missing_value=np.nan) -> Tuple[ndarray, ndarray]:
    """
    Linear Interpolation of missing values

    :param x_array: array-like, the x-coords
    :param values: array-like, the y-coords
    :param missing_value: can be specified, standard = np.nan
    :return: array where missing values are replaced by linear interpolation
    """
    # missing_value zu np.nan konvertieren (missing_value=0 zu np.nan konvertieren)
    if missing_value != np.nan:
        values = np.where(values == missing_value, np.nan, values)

    values = values.astype(float)

    # Nullwerte identifizieren
    ok = ~np.isnan(values)
    xp = ok.ravel().nonzero()[0]
    fp = values[~np.isnan(values)]
    x = np.isnan(values).ravel().nonzero()[0]

    # lineare Interpolation mit gültigen Nachbarn durchführen
    values[np.isnan(values)] = np.interp(x, xp, fp)
    return x_array, values


# FILTER 3
def moving_average(x_array: ndarray, values: ndarray, function, window_size: int) -> Tuple[ndarray, ndarray]:
    """
    Calculates the moving average of the function. If the values are sampled irregulary, the function approximates the
    filter function with a median of distances.

    :param x_array: array_like, the x-coords
    :param values: array_like, the y-coords
    :param function: values of filter function with length window_size
    :param window_size: size of the given filter function
    :raises ValueError: if size of data (y_array) < window_size (length of filter)
    :raises ValueError: if window size is <= 0
    :return: x_array and new y_array, that contains the data points filtered by a moving average with the given function
    """

    func_dict = {0: gauss_filter, 1: box_filter, 2: triangle_filter}

    if type(function) == int or type(function) == float:
        if not (0 <= function < 3):
            raise ValueError(f"{function} given, expected: 0: gauss_filter, 1: box_filter, 2: triangle_filter")

        function = func_dict[int(function)]

    if x_array[-1] - x_array[0] < window_size:
        raise ValueError("The given interval can't be smaller than the window size")

    if window_size <= 0:
        raise ValueError("Window_size must be larger than zero")

    if window_size % 2 == 0:
        window_size += 1

    variance = window_size * 2 / 3

    res = np.zeros(values.size)
    for i in range(values.size):
        x = x_array[i]
        min = x - window_size / 2
        max = x + window_size / 2
        x_min = np.searchsorted(x_array, min)
        x_max = np.searchsorted(x_array, max, 'right')
        y_vals = values[x_min:x_max]
        x_vals = function(x_array[x_min:x_max] - x, window_size, variance, x)
        res[i] = sum(y_vals * x_vals)

    return x_array, res


def gauss_filter(x_array, window_size, variance, x):
    gaussian = np.exp(-(x_array / variance) ** 2 / 2)
    gaussian /= sum(gaussian)
    return gaussian


def box_filter(x_array, window_size, variance, x):
    return np.array([1 for i in range(x_array.size)]) / x_array.size


def triangle_filter(x_array, window_size, variance, x):
    x1 = x_array[np.where(x_array < 0)] + window_size / 2
    x2 = window_size / 2 - x_array[np.where(x_array >= 0)]
    x = np.append(x1, x2)
    x = x / sum(x)
    return x


# FILTER 4
def adaptive_smoothing_filter(x_array: np.ndarray, values: np.ndarray, window_size: int) -> Tuple[np.ndarray, np.ndarray]:
    """
    Adaptive Smoothing

    :param x_array: array_like, the x-coords (usually timestamps)
    :param values: array_like, the y-coords
    :param window_size: Size of gaussian distribution with estimated variance

    :raises ValueError: if window_size < 0

    :return: float ndarray Calculates the time interval based convolution with a guassian filter
    with estimated variance, same shape as x.
    """
    n = len(values)
    filtered = np.copy(values)
    if window_size <= 0:
        raise ValueError("Window_size must be larger than zero")
    # half window size
    half_window_size = int(np.ceil(window_size / 2))
    for i in range(n):
        # calv interval
        ymin = max(0, i - half_window_size)
        ymax = min(n - 1, i + half_window_size)
        interval_size = ymax - ymin + 1
        # Correct Time Interval
        y_val = values[ymin:ymax + 1]
        # Maximum Likelihood Estimation Variance
        sigma = np.var(y_val)
        if sigma != 0:
            # Create gaussian distribution
            gx = np.linspace(interval_size / -2.0, interval_size / 2.0, num=interval_size)
            gaussian = np.exp(-(gx / sigma) ** 2 / 2)
            gaussian /= sum(gaussian)
            # Convolve Result with gaussian (Gaussian distribution is symmetric)
            filtered[i] = np.dot(y_val, gaussian)
    return x_array, filtered


# FILTER 5
def peak_removal(x_values: np.ndarray, y_values: np.ndarray, repetition=1) -> Tuple[ndarray, ndarray]:
    """
    Removes Peaks from values and replaces them with the nearest neighbor

    :param x_values: numpy array of x_values like time, day, etc.
    :param y_values: numpy array of y_values like speed, gps, etc.
    :param repetition: possible repetition for multiple, iterative peak removal
    :raises ValueError: if repetition < 1
    :return: returns the original and filtered data
    """

    def removal(x_values: ndarray, y_values: ndarray) -> Tuple[ndarray, ndarray]:
        # Remove "high"-peaks
        peaks, _ = find_peaks(y_values, prominence=1, wlen=2)
        m = np.zeros(x_values.shape, dtype=bool)
        m[peaks] = True

        peaks_deleted_x = x_values[~m]
        peaks_deleted_y = y_values[~m]
        peaks_points_to_resample = x_values[m]

        _, peaks_resampled_y = resampling_nearest(peaks_deleted_x, peaks_deleted_y, peaks_points_to_resample)
        y_values[peaks] = peaks_resampled_y

        # Remove "low"-peaks
        negpeaks, _ = find_peaks(-y_values)
        m = np.zeros(x_values.shape, dtype=bool)
        m[negpeaks] = True

        neg_peaks_deleted_x = x_values[~m]
        neg_peaks_deleted_y = y_values[~m]
        neg_peaks_points_to_resample = x_values[m]

        _, neg_peaks_resampled_y = resampling_nearest(neg_peaks_deleted_x, neg_peaks_deleted_y,
                                                      neg_peaks_points_to_resample)
        y_values[negpeaks] = neg_peaks_resampled_y

        return x_values, y_values

    if repetition < 1:
        raise ValueError("value of repetition has to be >= 1")

    x_val, y_val = np.copy(x_values), np.copy(y_values)
    i = 0
    while i < repetition:
        x_val, y_val = removal(x_val, y_val)
        i += 1

    return x_val, y_val


# FILTER 6
def filter_derivative_smoothing(x_array: ndarray, values: ndarray, function, window_size: int) -> Tuple[
    ndarray, ndarray]:
    """
    Smoothes the numerical derivate and returns retransformed values

    :param x_array: array-like, x-coords
    :param values: array-like, y-coords
    :param function: values of filter function with length window_size
    :param window_size: size of the given filter function
    :raises ValueError: if length of data == 1
    :return: x_array and smoothed values
    """

    func_dict = {0: gauss_filter, 1: box_filter, 2: triangle_filter}

    if type(function) == int or type(function) == float:
        if not (0 <= function < 3):
            raise ValueError(f"{function} given, expected: 0: gauss_filter, 1: box_filter, 2: triangle_filter")

        function = func_dict[int(function)]

    if x_array.size == 1:
        raise ValueError("The given data set must contain more than 1 Element")

    timestamps_distances = np.diff(x_array)
    derivative = np.diff(values) / timestamps_distances
    smoothed = moving_average(x_array[:-1], derivative, function, window_size)
    fun_min = np.min(values)
    fun_max = np.max(values)
    integral = (np.cumsum(smoothed[1]) + values[0])
    integral_min = np.min(integral)
    integral_max = np.max(integral)
    c = np.mean(values[:-1] - integral)
    k = (integral_max - integral_min) / (fun_max - fun_min)
    return x_array[:-1], (integral - c) / k


# FILTER 7
def resampling_nearest(x_array: ndarray, values: ndarray, x_to_interpolate: ndarray) -> Tuple[ndarray, ndarray]:
    """
    Resamples given points with nearest neighbor

    :param x_array: ndarray
    The x-coordinates of the data points
    :param values: ndarray
    The y-coordinates of the data points, same length as x_array
    :param x_to_interpolate: ndarray
    The x-coordinates at which to evaluate the interpolated value
    :raises ValueError: if lenghts or shapes don't match or data size == 0
    :return: two arrays
    first one is x_to_interpolate
    second one contains resampled values
    """

    if type(x_to_interpolate) == int or type(x_to_interpolate) == float:
        x_to_interpolate = np.linspace(x_array[0], x_array[-1], num=int(x_to_interpolate))

    def find_nearest_index(array, value):
        """returns the smallest neighbouring index with minimum distance"""
        return np.abs(array - value).argmin()

    if len(x_array) != len(values):
        raise ValueError("unequal length of x_values and y_values")
    if x_array.ndim != 1 or values.ndim != 1 or x_to_interpolate.ndim != 1:
        raise ValueError("the given arrays have to be 1d")
    if x_array.size == 0 or values.size == 0:
        raise ValueError("x_values and y_values can not be empty")

    result = np.zeros(len(x_to_interpolate))

    # über x_tointerpolate iterieren
    for i, elem in enumerate(x_to_interpolate):
        # nächsten x Werte in x_array
        nearest_index = find_nearest_index(x_array, elem)
        # dessen y Wert einsetzen
        result[i] = values[nearest_index]

    return x_to_interpolate, result


# FILTER 8
def resampling_linear(x_array: ndarray, values: ndarray, x_to_interpolate: ndarray, left=None, right=None, period=None) \
        -> Tuple[ndarray, ndarray]:
    """
    Resamples given points with linear Interpolation

    :param x_to_interpolate: array_like
    The x-coordinates at which to evaluate the interpolated value

    :param x_array: 1-D sequence of floats
        The x-coordinates of the data points, must be increasing if argument period is not specified.
        Otherwise, x_array is internally sorted after normalizing the periodic boundaries with xp = xp % period.

    :param values: 1-D sequence of float or complex
        The y-coordinates of the data points, same length as x_array.

    :param left: optional float or complex corresponding to values
        Value to return for x < x_array[0], default is values[0].

    :param right: optional float or complex corresponding to values
        Value to return for x > x_array[-1], default is values[-1].

    :param period: None or float, optional
        A period for the x-coordinates.
        This parameter allows the proper interpolation of angular x-coordinates.
        Parameters left and right are ignored if period is specified.

    :raises ValueError: if x_array and values have different length If x_array or values are not 1-D sequences If period == 0

    :return: float or complex (corresponding to fp) or ndarray
    The interpolated values, same shape as x_to_interpolate.
    """

    if type(x_to_interpolate) == int or type(x_to_interpolate) == float:
        x_to_interpolate = np.linspace(x_array[0], x_array[-1], num=int(x_to_interpolate))

    return x_to_interpolate, np.interp(x_to_interpolate, x_array, values, left, right, period)
