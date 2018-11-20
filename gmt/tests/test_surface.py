"""
Tests for surface
"""
import os

import pytest
import xarray as xr

from .. import surface
from .. import which
from ..datasets import load_tut_ship
from ..exceptions import GMTInvalidInput
from ..helpers import data_kind

TEST_DATA_DIR = os.path.join(os.path.dirname(__file__), "data")
TEMP_GRID = os.path.join(TEST_DATA_DIR, "tmp_grid.nc")


def test_surface_input_file():
    """
    Run surface by passing in a filename
    """
    fname = which("@tut_ship.xyz", download="c")
    output = surface(data=fname, I="5m", R="245/255/20/30")
    assert isinstance(output, xr.Dataset)
    return output


def test_surface_input_data_array():
    """
    Run surface by passing in a numpy array into data
    """
    ship_data = load_tut_ship()
    data = ship_data.values  # convert pandas.DataFrame to numpy.ndarray
    output = surface(data=data, I="5m", R="245/255/20/30")
    assert isinstance(output, xr.Dataset)
    return output


def test_surface_input_xyz():
    """
    Run surface by passing in x, y, z numpy.ndarrays individually
    """
    ship_data = load_tut_ship()
    output = surface(
        x=ship_data.x, y=ship_data.y, z=ship_data.z, I="5m", R="245/255/20/30"
    )
    assert isinstance(output, xr.Dataset)
    return output


def test_surface_input_xy_no_z():
    """
    Run surface by passing in x and y, but no z
    """
    ship_data = load_tut_ship()
    with pytest.raises(GMTInvalidInput):
        surface(x=ship_data.x, y=ship_data.y, I="5m", R="245/255/20/30")


def test_surface_wrong_kind_of_input():
    """
    Run surface using grid input that is not file/matrix/vectors
    """
    ship_data = load_tut_ship()
    data = ship_data.z.to_xarray()  # convert pandas.Series to xarray.DataArray
    assert data_kind(data) == "grid"
    with pytest.raises(GMTInvalidInput):
        surface(data=data, I="5m", R="245/255/20/30")


def test_surface_g_outfile_param():
    """
    Run surface with the -Goutputfile.nc parameter.
    """
    ship_data = load_tut_ship()
    data = ship_data.values  # convert pandas.DataFrame to numpy.ndarray
    try:
        output = surface(data=data, I="5m", R="245/255/20/30", G=TEMP_GRID)
        assert os.path.exists(TEMP_GRID)
        grid = xr.open_dataset(TEMP_GRID)
        assert output == grid  # check that original output is same as that from file
    finally:
        os.remove(path=TEMP_GRID)
    return output
