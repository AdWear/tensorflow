"""Tests for tensorflow.ops.argmax_op."""
import tensorflow.python.platform

import numpy as np
import tensorflow as tf

class ArgMaxTest(tf.test.TestCase):

  def _testArg(self, method, x, dimension,
               expected_values, use_gpu=False, expected_err_re=None):
    with self.test_session(use_gpu=use_gpu):
      ans = method(x, dimension=dimension)
      if expected_err_re is None:
        tf_ans = ans.eval()
        self.assertAllEqual(tf_ans, expected_values)
        self.assertShapeEqual(expected_values, ans)
      else:
        with self.assertRaisesOpError(expected_err_re):
          ans.eval()

  def _testBothArg(self, method, x, dimension,
                   expected_values, expected_err_re=None):
    self._testArg(method, x, dimension,
                  expected_values, True, expected_err_re)
    self._testArg(method, x, dimension,
                  expected_values, False, expected_err_re)

  def _testBasic(self, dtype):
    x = np.asarray(100*np.random.randn(200), dtype=dtype)

    # Check that argmin and argmax match numpy along the primary
    # dimension
    self._testBothArg(tf.argmax, x, 0, x.argmax())
    self._testBothArg(tf.argmin, x, 0, x.argmin())

  def _testDim(self, dtype):
    x = np.asarray(100*np.random.randn(3, 2, 4, 5, 6), dtype=dtype)

    # Check that argmin and argmax match numpy along all dimensions
    for dim in range(5):
      self._testBothArg(tf.argmax, x, dim, x.argmax(dim))
      self._testBothArg(tf.argmin, x, dim, x.argmin(dim))

  def testFloat(self):
    self._testBasic(np.float32)
    self._testDim(np.float32)

  def testDouble(self):
    self._testBasic(np.float64)
    self._testDim(np.float64)

  def testInt32(self):
    self._testBasic(np.int32)
    self._testDim(np.int32)

  def testInt64(self):
    self._testBasic(np.int64)
    self._testDim(np.int64)

if __name__ == "__main__":
  tf.test.main()
