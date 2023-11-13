import numpy as np
import pytest

from filter_functions import *

x_array1 = np.array(range(0, 10))
y_array1 = np.array([5, 2, 0, 4, 3, 6, 2, 1, 0, 5])


def test_concat_function():
    x1, y1 = moving_average(x_array1, y_array1, triangle_filter, 6)
    x2, y2 = clipping_filter(x1, y1, 1, 5)
    x3, y3 = filter_derivative_smoothing(x2, y2, box_filter, 6)

    y_array_with_nans = np.array([5, np.nan, 0, 4, np.nan, np.nan, 2, 1, 0, 5])
    x4, y4 = interpolate_nan(x_array1, y_array_with_nans)
    x5, y5 = resampling_linear(x4, y4, np.array([1.5, 2.5, 3.5, 4.5, 5.5]))
    x6, y6 = adaptive_smoothing_filter(x5, y5, 3)
    x7, y7 = resampling_nearest(x_array1, y_array1, np.array([1.5, 2.5, 3.5, 4.5, 5.5]))
    x8, y8 = peak_removal(x7, y7)

    assert np.all(np.equal(x2, concat_funct(x_array1, y_array1, [moving_average, clipping_filter],
                                            [[triangle_filter, 6], [1, 5]])[0]))
    assert np.all(np.equal(y2, concat_funct(x_array1, y_array1, [moving_average, clipping_filter],
                                            [[triangle_filter, 6], [1, 5]])[1]))
    assert np.all(
        np.equal(y3, concat_funct(x_array1, y_array1, [moving_average, clipping_filter, filter_derivative_smoothing],
                                  [[triangle_filter, 6], [1, 5], [box_filter, 6]])[1]))
    assert np.all(np.equal(y5, concat_funct(x_array1, y_array_with_nans, [interpolate_nan, resampling_linear],
                                            [[], [np.array([1.5, 2.5, 3.5, 4.5, 5.5])]])[1]))
    assert np.all(np.equal(y6, concat_funct(x_array1, y_array_with_nans,
                                            [interpolate_nan, resampling_linear, adaptive_smoothing_filter],
                                            [[], [np.array([1.5, 2.5, 3.5, 4.5, 5.5])], [3]])[1]))
    assert np.all(np.equal(y8, concat_funct(x_array1, y_array1, [resampling_nearest, peak_removal],
                                            [[np.array([1.5, 2.5, 3.5, 4.5, 5.5])], []])[1]))
    with pytest.raises(ValueError):
        concat_funct(x_array1, np.append(np.array([1]), y_array1), [clipping_filter], [[1, 5]])
    with pytest.raises(ValueError):
        concat_funct(np.array([]), np.array([]), [clipping_filter], [[1, 5]])
    with pytest.raises(ValueError):
        concat_funct(x_array1, y_array1, [], [])
    with pytest.raises(ValueError):
        concat_funct(x_array1, y_array1, [moving_average, clipping_filter], [[gauss_filter, 3]])
    with pytest.raises(ValueError):
        concat_funct(np.array([1, 2, 4, 3]), np.array([5, 5, 5, 5]), [clipping_filter], [[1, 5]])
    with pytest.raises(ValueError):
        concat_funct(np.array([1, 2, 3, 3]), np.array([5, 5, 5, 5]), [clipping_filter], [[1, 5]])
    with pytest.raises(Exception):
        concat_funct(np.array([1, 2, 3, 4]), np.array([1, 2, 3, 4]), [moving_average], [[gauss_filter, 5]])


# FILTER 1:
def test_clipping_filter():
    """tests the clipping filter function, filter function 1"""
    x_res, y_res = clipping_filter(x_array1, y_array1, 1, 4)
    # Test 1: x_array unchanged
    assert np.all(np.equal(x_res, x_array1))
    # Test 1.1: inputs unchanged
    assert np.array_equal(x_array1, np.array(range(10)))
    assert np.array_equal(y_array1, np.array([5, 2, 0, 4, 3, 6, 2, 1, 0, 5]))
    # Test 2: correct clip
    assert np.all(np.equal(y_res, np.array([4, 2, 1, 4, 3, 4, 2, 1, 1, 4])))
    _, y_res2 = clipping_filter(np.array([i / 10 for i in range(300)]), np.random.random_sample(300), 0.2, 0.4)
    assert np.all(y_res2 <= 0.4)
    assert np.all(y_res2 >= 0.2)
    # Test 3: output sizes with same length
    assert np.size(x_res) == np.size(y_res)
    # Test 4: inputs of size 1
    assert np.array_equal(clipping_filter(np.array([1]), np.array([1]), 0, 2)[1], np.array([1]))
    # Test 5: minval > maxval
    with pytest.raises(ValueError):
        clipping_filter(x_array1, y_array1, 2, 1)


# FILTER 2
def test_interpolate_nan():
    # Test 0: check that correctly interpolated with missing value = np.nan
    x_data0 = np.array([1, 2, 3, 4, 5])
    y_data0 = np.array([2, 5, np.nan, 8, 1])
    y_interpolated0 = np.array([2, 5, 6.5, 8, 1])
    assert np.array_equal(interpolate_nan(x_data0, y_data0)[1], y_interpolated0)

    # Test 0.1: check negative time:
    assert np.array_equal(interpolate_nan(np.array(range(-5, 0)), y_data0)[1], y_interpolated0)

    # Test 1: check that no interpolation is happening
    nan1 = 0
    y_interpolated1 = np.array([2, 5, np.nan, 8, 1])
    assert not np.array_equal(interpolate_nan(x_data0, y_data0, nan1)[1], y_interpolated1)

    # Test 2: check that correctly interpolated with missing value = 0
    nan2 = 0
    y_data2 = np.array([2, 5, 0, 8, 1])
    y_interpolated2 = np.array([2, 5, 6.5, 8, 1])
    assert np.array_equal(interpolate_nan(x_data0, y_data2, nan2)[1], y_interpolated2)

    # Test 2: check that correctly interpolated with missing value = 0
    nan80 = None
    y_data80 = np.array([2, 5, None, 8, 1])
    y_interpolated80 = np.array([2, 5, 6.5, 8, 1])
    assert np.array_equal(interpolate_nan(x_data0, y_data80, nan80)[1], y_interpolated80)

    # Test 2.1: check inputs not changed
    assert np.array_equal(x_data0, np.array([1, 2, 3, 4, 5]))
    assert np.array_equal(y_data2, np.array([2, 5, 0, 8, 1]))

    # Test 3: np.nan on edges -> np.nan becomes nearest neighbor:
    y_data3 = np.array([np.nan, 5, 6.5, 8, 1])
    y_interpolated3 = np.array([5, 5, 6.5, 8, 1])
    assert np.array_equal(interpolate_nan(x_data0, y_data3)[1], y_interpolated3)
    y_data3 = np.array([2, 5, 6.5, 8, np.nan])
    y_interpolated3 = np.array([2, 5, 6.5, 8, 8])
    assert np.array_equal(interpolate_nan(x_data0, y_data3)[1], y_interpolated3)

    # Test 4: input arrays with one elem
    assert np.array_equal(interpolate_nan(np.array([1]), np.array([1]))[1], np.array([1]))


# FILTER 3:
def test_moving_average():
    """test moving_average function, filter function 3"""
    x_array = np.arange(100)
    y_array = np.array([5 for i in range(100)])
    x_res, y_res = moving_average(x_array, y_array, gauss_filter, 6)
    x_res2, y_res2 = moving_average(x_array, y_array, box_filter, 6)
    x_res3, y_res3 = moving_average(x_array, y_array, triangle_filter, 6)

    assert np.all(np.isclose(np.array([5 for i in range(92)]), y_res[4:96]))
    assert x_res.size == x_array.size and y_res.size == y_array.size

    assert np.all(np.isclose(np.array([5 for i in range(92)]), y_res2[4:96]))
    assert x_res2.size == x_array.size and y_res2.size == y_array.size

    assert np.all(np.isclose(np.array([5 for i in range(92)]), y_res3[4:96], 0.02))
    assert x_res3.size == x_array.size and y_res3.size == y_array.size

    with pytest.raises(ValueError):
        moving_average(np.array([1, 2, 3, 4]), np.array([1 for i in range(4)]), gauss_filter, 5)


# FILTER 4
def test_adaptive_smoothing_filter():
    # Test 1: negative window_size
    with pytest.raises(ValueError):
        adaptive_smoothing_filter(x_array1, y_array1, -1)

    # Test 2: same length of results
    x_res1, y_res1 = adaptive_smoothing_filter(x_array1, y_array1, 3)
    assert np.size(x_res1) == np.size(y_res1)

    # Test 3: window_size > arrays
    try:
        adaptive_smoothing_filter(x_array1, y_array1, 15)
    except Exception as exc:
        assert False, f"bigger window size raised exception {exc}"

    # Test 4: input arrays of length 1
    assert adaptive_smoothing_filter(np.array(range(1)), np.array(range(1)), 1)[1] == np.array([0])

    # Test 5: values with variance = 0
    values = np.array([5 for i in range(10)])
    assert np.array_equal(adaptive_smoothing_filter(np.array(range(10)), values, 3)[1], values)

    # Test 6: inputs not changed
    assert np.array_equal(x_array1, np.array(range(0, 10)))
    assert np.array_equal(y_array1, np.array([5, 2, 0, 4, 3, 6, 2, 1, 0, 5]))


# FILTER 5
def test_peak_removal():
    """tests if peaks get removed from a graph"""
    small_x = np.array(range(0, 10))
    small_y = np.array([9, 0, 1, 2, 5, 3, 3, 1, 2, 4])

    x_smooth, y_smooth = peak_removal(small_x, small_y)

    # Test 1: input x and y arrays aren't changed
    assert np.array_equal(small_x, np.array(range(0, 10)))
    assert np.array_equal(small_y, np.array([9, 0, 1, 2, 5, 3, 3, 1, 2, 4]))

    # Test 2: correct peak smoothing
    assert np.all(np.equal(y_smooth, np.array([9, 9, 1, 2, 2, 3, 3, 3, 2, 4])))

    # Test 3: correct peak smoothing, iterations > 1
    x_smooth, y_smooth = peak_removal(small_x, small_y, 2)
    assert np.all(np.equal(y_smooth, np.array([9, 9, 9, 2, 2, 3, 3, 3, 3, 4])))

    # Test 4: results with same lengths
    assert np.size(x_smooth) == np.size(y_smooth)

    # Test 5: input arrays with length 1
    assert np.array_equal(peak_removal(np.array(range(1)), np.array(range(1)))[1], np.array([0]))


# FILTER 6:
def test_filter_derivative_smoothing():
    """test filter_derivative_smoothing, filter function 6"""

    # Test 1: Length Test and plot
    y_array1 = 5 * np.sin(np.arange(500) / 10) + np.hstack([np.random.randn(250), 4 * np.random.randn(250)])
    x_res, y_res = filter_derivative_smoothing(np.array(range(500)), y_array1, gauss_filter, 5)
    assert len(y_res) == len(y_array1) - 1
    # plt.plot(np.array(range(500)), y_array1)
    # plt.plot(x_res, y_res)
    # plt.show()

    # Test 2:
    with pytest.raises(ValueError):
        filter_derivative_smoothing(np.array([1]), np.array([1]), gauss_filter, 50)


x_to_interpolate = np.array([1.5, 2.5, 3.5, 4.5])
x_array2 = np.array([1, 2, 3, 4, 5, 6])
y_array2 = np.array([1, 2, 3, 4, 5, 6])


# FILTER 7
def test_resampling_nearest_errors():
    xp_too_long = np.array([1, 2, 3, 4, 5, 6, 7])

    with pytest.raises(ValueError):
        resampling_nearest(x_to_interpolate, xp_too_long, y_array2)

    fp_too_long = xp_too_long

    with pytest.raises(ValueError):
        resampling_nearest(x_to_interpolate, x_array2, fp_too_long)

    xp_2_dim = np.array([[1, 2, 3, 4, 5, 6], [1, 2, 3, 4, 5, 6]])
    fp_2_dim = xp_2_dim

    with pytest.raises(ValueError):
        resampling_nearest(x_to_interpolate, xp_2_dim, fp_2_dim)

    with pytest.raises(ValueError):
        resampling_nearest(np.array([]), np.array([]), x_to_interpolate)


# FILTER 7
def test_resample_nearest():
    x = np.array([1.5, 2.5, 3.5, 4.5, 5.5, 6.5])
    x_neg = -x
    x_to_interpolate = np.array([1, 2, 3, 4, 5, 6])
    y_values = np.array([1, 2, 3, 4, 5, 6])
    y_neg = -y_values
    # Test 1: normal function call
    assert (resampling_nearest(x, y_values, x_to_interpolate)[1] == np.array([1, 1, 2, 3, 4, 5])).all()
    # Test 1.1: input not changed
    assert np.array_equal(x, np.array([1.5, 2.5, 3.5, 4.5, 5.5, 6.5]))
    assert np.array_equal(y_values, np.array([1, 2, 3, 4, 5, 6]))
    assert np.array_equal(x_to_interpolate, np.array([1, 2, 3, 4, 5, 6]))
    # Test 2: empty output array
    assert (resampling_nearest(x, y_values, np.array([]))[1] == np.array([])).all()
    # Test 3: negative x_values
    assert (resampling_nearest(x_neg, y_values, x_to_interpolate)[1] == np.ones(len(x_to_interpolate))).all()
    # Test 4: negative y_values
    x_res4, y_res4 = resampling_nearest(x, y_neg, x_to_interpolate)
    assert (resampling_nearest(x, y_neg, x_to_interpolate))
    # Test 5: outputs with same length
    assert np.size(x_res4) == np.size(y_res4)
    # Test 6: input size 1
    assert np.array_equal(resampling_nearest(np.array([1]), np.array([1]), np.array([0]))[1], np.array([1]))


# FILTER 8
def test_resampling_linear_functionality():
    x = np.array([1.5, 2.5, 3.5, 4.5, 5.5, 6.5])
    x_neg = -x
    x_to_interpolate = np.array([1, 2, 3, 4, 5, 6])
    y_values = np.array([1, 2, 3, 4, 5, 6])
    y_neg = -y_values
    # Test 1: normal function call
    assert (resampling_linear(x, y_values, x_to_interpolate)[1] == np.array([1., 1.5, 2.5, 3.5, 4.5, 5.5])).all()
    # Test 1.1: input not changed
    assert np.array_equal(x, np.array([1.5, 2.5, 3.5, 4.5, 5.5, 6.5]))
    assert np.array_equal(y_values, np.array([1, 2, 3, 4, 5, 6]))
    assert np.array_equal(x_to_interpolate, np.array([1, 2, 3, 4, 5, 6]))
    # Test 2: empty output array
    assert (resampling_linear(x, y_values, np.array([]))[1] == np.array([])).all()
    # Test 3: negative x_values
    assert (resampling_linear(x_neg, y_values, x_to_interpolate)[1] == np.array([6., 6., 6., 6., 6., 6.])).all()
    # Test 4: negative y_values
    x_res4, y_res4 = resampling_linear(x, y_neg, x_to_interpolate)
    assert (y_res4 == np.array([-1., -1.5, -2.5, -3.5, -4.5, -5.5])).all()
    # Test 5: outputs with same length
    assert np.size(x_res4) == np.size(y_res4)
    # Test 6: input size 1
    assert np.array_equal(resampling_nearest(np.array([1]), np.array([1]), np.array([0]))[1], np.array([1]))


# FILTER 8
def test_resampling_linear_errors():
    xp_too_long = np.array([1, 2, 3, 4, 5, 6, 7])

    with pytest.raises(ValueError):
        resampling_linear(x_to_interpolate, xp_too_long, y_array2)

    fp_too_long = xp_too_long

    with pytest.raises(ValueError):
        resampling_linear(x_to_interpolate, x_array2, fp_too_long)

    xp_2_dim = np.array([[1, 2, 3, 4, 5, 6], [1, 2, 3, 4, 5, 6]])
    fp_2_dim = xp_2_dim

    with pytest.raises(ValueError):
        resampling_linear(x_to_interpolate, xp_2_dim, fp_2_dim)

    with pytest.raises(ValueError):
        resampling_linear(x_to_interpolate, x_array2, y_array2, period=0)


def test_moving_average_new():
    x_array = np.arange(100)
    y_array = np.array([5 for i in range(100)])
    x_res, y_res = moving_average(x_array, y_array, 0, 6)
    x_res2, y_res2 = moving_average(x_array, y_array, 1, 6)
    x_res3, y_res3 = moving_average(x_array, y_array, 2, 6)

    assert np.all(np.isclose(np.array([5 for i in range(92)]), y_res[4:96]))
    assert x_res.size == x_array.size and y_res.size == y_array.size

    assert np.all(np.isclose(np.array([5 for i in range(92)]), y_res2[4:96]))
    assert x_res2.size == x_array.size and y_res2.size == y_array.size

    assert np.all(np.isclose(np.array([5 for i in range(92)]), y_res3[4:96], 0.02))
    assert x_res3.size == x_array.size and y_res3.size == y_array.size

    with pytest.raises(ValueError):
        moving_average(np.array([1, 2, 3, 4]), np.array([1 for i in range(4)]), gauss_filter, 5)


def test_derivative_smoothing():
    # Test 1: Length Test and plot
    y_array1 = 5 * np.sin(np.arange(500) / 10) + np.hstack([np.random.randn(250), 4 * np.random.randn(250)])
    x_res, y_res = filter_derivative_smoothing(np.array(range(500)), y_array1, 0, 5)
    assert len(y_res) == len(y_array1) - 1
    # plt.plot(np.array(range(500)), y_array1)
    # plt.plot(x_res, y_res)
    # plt.show()

    # Test 2:
    with pytest.raises(ValueError):
        filter_derivative_smoothing(np.array([1]), np.array([1]), 0, 50)


def test_resample_nearest_new():
    x = np.array([1.5, 2.5, 3.5, 4.5, 5.5, 6.5])
    x_neg = -x
    y_values = np.array([1, 2, 3, 4, 5, 6])
    y_neg = -y_values
    # Test 1: normal function call
    assert (resampling_nearest(x, y_values, 6)[1] == np.array([1.0, 2.0, 3.0, 4.0, 5.0, 6.0])).all()
    assert (resampling_nearest(x, y_values, 6.0)[1] == np.array([1.0, 2.0, 3.0, 4.0, 5.0, 6.0])).all()
    # Test 1.1: input not changed
    assert np.array_equal(x, np.array([1.5, 2.5, 3.5, 4.5, 5.5, 6.5]))
    assert np.array_equal(y_values, np.array([1, 2, 3, 4, 5, 6]))
    assert np.array_equal(np.linspace(1, 6, num=6), np.array([1, 2, 3, 4, 5, 6]))
    # Test 2: empty output array
    assert (resampling_nearest(x, y_values, 0)[1] == np.array([])).all()
    # Test 3: negative x_values
    assert (resampling_nearest(x_neg, y_values, 6)[1] == np.array([1.0, 2.0, 3.0, 4.0, 5.0, 6.0])).all()
    # Test 4: negative y_values
    x_res4, y_res4 = resampling_nearest(x, y_neg, 6)
    assert (resampling_nearest(x, y_neg, 6))
    # Test 5: outputs with same length
    assert np.size(x_res4) == np.size(y_res4)
    # Test 6: input size 1
    assert np.array_equal(resampling_nearest(np.array([1]), np.array([1]), 1)[1], np.array([1]))


def test_resampling_linear_functionality_new():
    x = np.array([1.5, 2.5, 3.5, 4.5, 5.5, 6.5])
    x_neg = np.array([-6.5, -5.5, -4.5, -3.5, -2.5, -1.5])
    y_values = np.array([1, 2, 3, 4, 5, 6])
    y_neg = -y_values
    # Test 1: normal function call
    assert (resampling_linear(x, y_values, 6)[1] == np.array([1., 2., 3., 4., 5., 6.])).all()
    # Test 1.1: input not changed
    assert np.array_equal(x, np.array([1.5, 2.5, 3.5, 4.5, 5.5, 6.5]))
    assert np.array_equal(y_values, np.array([1, 2, 3, 4, 5, 6]))
    assert np.array_equal(np.linspace(1, 6, num=6), np.array([1, 2, 3, 4, 5, 6]))
    # Test 2: empty output array
    assert (resampling_linear(x, y_values, 0)[1] == np.array([])).all()
    # Test 3: negative x_values
    assert (resampling_linear(x_neg, y_values, 6)[1] == np.array([1., 2., 3., 4., 5., 6.])).all()
    # Test 4: negative y_values
    x_res4, y_res4 = resampling_linear(x, y_neg, 6)
    print(y_res4)
    assert (y_res4 == np.array([-1., -2., -3., -4., -5., -6.])).all()
    # Test 5: outputs with same length
    assert np.size(x_res4) == np.size(y_res4)
    # Test 6: input size 1
    assert np.array_equal(resampling_nearest(np.array([1]), np.array([1]), np.array([0]))[1], np.array([1]))
