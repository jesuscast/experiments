# Copyright (C) 2013 Maximilian Nickel <mnick@mit.edu>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.


import numpy

def interpolate(x, y, x_new, axis=-1, out=None):
  """Return interpolated data using Akima's method.

  This Python implementation is inspired by the Matlab(r) code by
  N. Shamsundar. It lacks certain capabilities of the C implementation
  such as the output array argument and interpolation along an axis of a
  multidimensional data array.

  Parameters
  ----------
  x : array like
    1D array of monotonically increasing real values.
  y : array like
    N-D array of real values. y's length along the interpolation
    axis must be equal to the length of x.
  x_new : array like
    New independent variables.
  axis : int
    Specifies axis of y along which to interpolate. Interpolation
    defaults to last axis of y.
  out : array
    Optional array to receive results. Dimension at axis must equal
    length of x.

  Examples
  --------
  >>> interpolate([0, 1, 2], [0, 0, 1], [0.5, 1.5])
  array([-0.125,  0.375])
  >>> x = numpy.sort(numpy.random.random(10) * 10)
  >>> y = numpy.random.normal(0.0, 0.1, size=len(x))
  >>> z = interpolate(x, y, x)
  >>> numpy.allclose(y, z)
  True
  >>> x = x[:10]
  >>> y = numpy.reshape(y, (10, -1))
  >>> z = numpy.reshape(y, (10, -1))
  >>> interpolate(x, y, x, axis=0, out=z)
  >>> numpy.allclose(y, z)
  True

  """
  x = numpy.array(x, dtype=numpy.float64, copy=True)
  y = numpy.array(y, dtype=numpy.float64, copy=True)
  xi = numpy.array(x_new, dtype=numpy.float64, copy=True)

  if axis != -1 or out is not None or y.ndim != 1:
    raise NotImplementedError("implemented in C extension module")

  if x.ndim != 1 or xi.ndim != 1:
    raise ValueError("x-arrays must be one dimensional")

  n = len(x)
  if n < 3:
    raise ValueError("array too small")
  if n != y.shape[axis]:
    raise ValueError("size of x-array must match data shape")

  dx = numpy.diff(x)
  for i in range(len(dx)):
    if dx[i] == 0 and i != 0:
      dx[i] = 0.000001
      x[i] = x[i-1] + 0.000001
  if any(dx <= 0.0):
    raise ValueError("x-axis not valid")

  if any(xi < x[0]) or any(xi > x[-1]):
    raise ValueError("interpolation x-axis out of bounds")

  m = numpy.diff(y) / dx
  mm = 2.0 * m[0] - m[1]
  mmm = 2.0 * mm - m[0]
  mp = 2.0 * m[n - 2] - m[n - 3]
  mpp = 2.0 * mp - m[n - 2]

  m1 = numpy.concatenate(([mmm], [mm], m, [mp], [mpp]))

  dm = numpy.abs(numpy.diff(m1))
  f1 = dm[2:n + 2]
  f2 = dm[0:n]
  f12 = f1 + f2

  ids = numpy.nonzero(f12 > 1e-9 * numpy.max(f12))[0]
  b = m1[1:n + 1]

  b[ids] = (f1[ids] * m1[ids + 1] + f2[ids] * m1[ids + 2]) / f12[ids]
  c = (3.0 * m - 2.0 * b[0:n - 1] - b[1:n]) / dx
  d = (b[0:n - 1] + b[1:n] - 2.0 * m) / dx ** 2

  bins = numpy.digitize(xi, x)
  bins = numpy.minimum(bins, n - 1) - 1
  bb = bins[0:len(xi)]
  wj = xi - x[bb]

  return ((wj * d[bb] + c[bb]) * wj + b[bb]) * wj + y[bb]