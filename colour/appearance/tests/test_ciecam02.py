# !/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Defines unit tests for :mod:`colour.appearance.ciecam02` module.
"""

from __future__ import division, unicode_literals

import numpy as np
from numpy.testing.utils import assert_allclose, assert_almost_equal
from colour.appearance.ciecam02 import (
    CIECAM02_InductionFactors,
    XYZ_to_CIECAM02, CIECAM02_Specification, CIECAM02_to_XYZ)
from colour.appearance.tests.common import ColourAppearanceModelTest

__author__ = 'Colour Developers'
__copyright__ = 'Copyright (C) 2013 - 2014 - Colour Developers'
__license__ = 'New BSD License - http://opensource.org/licenses/BSD-3-Clause'
__maintainer__ = 'Colour Developers'
__email__ = 'colour-science@googlegroups.com'
__status__ = 'Production'

__all__ = ['TestCIECAM02ColourAppearanceModelForward']


class TestCIECAM02ColourAppearanceModelForward(ColourAppearanceModelTest):
    """
    Defines :mod:`colour.appearance.ciecam02` module units tests methods for
    *CIECAM02* colour appearance model forward implementation.
    """

    FIXTURE_BASENAME = 'ciecam02.csv'

    OUTPUT_ATTRIBUTES = {'J': 'J',
                         'Q': 'Q',
                         'C': 'C',
                         'M': 'M',
                         'S': 's'}

    def output_specification_from_data(self, data):
        """
        Returns the *CIECAM02* colour appearance model output specification
        from given data.

        Parameters
        ----------
        data : list
            Fixture data.

        Returns
        -------
        CIECAM02_Specification
            *CIECAM02* colour appearance model specification.
        """

        XYZ = np.array([data['X'], data['Y'], data['Z']])
        XYZ_w = np.array([data['X_W'], data['Y_W'], data['Z_W']])

        specification = XYZ_to_CIECAM02(XYZ,
                                        XYZ_w,
                                        data['L_A'],
                                        data['Y_b'],
                                        CIECAM02_InductionFactors(data['F'],
                                                                  data['c'],
                                                                  data['N_c']))
        return specification


class TestCIECAM02ColourAppearanceModelReverse(ColourAppearanceModelTest):
    """
    Defines :mod:`colour.appearance.ciecam02` module units tests methods for
    *CIECAM02* colour appearance model reverse implementation.
    """

    FIXTURE_BASENAME = 'ciecam02.csv'

    OUTPUT_ATTRIBUTES = {'X': 0,
                         'Y': 1,
                         'Z': 2,
    }

    def get_output_specification_from_data(self, data):
        """
        Returns the *CIECAM02* colour appearance model output specification
        from given data.

        Parameters
        ----------
        data : list
            Fixture data.

        Returns
        -------
        CIECAM02_Specification
            *CIECAM02* colour appearance model specification.
        """

        specification = CIECAM02_Specification(data['J'],
                                               data['C'],
                                               data['H'],
                                               data['Q'],
                                               data['M'],
                                               data['S'],
                                               data['H'])

        XYZ_w = np.array([data['X_W'], data['Y_W'], data['Z_W']])

        specification = CIECAM02_to_XYZ(specification,
                                        XYZ_w,
                                        data['L_A'],
                                        data['Y_b'],
                                        CIECAM02_InductionFactors(data['F'],
                                                                  data['c'],
                                                                  data['N_c']))
        return specification



    def check_specification_attribute(self, case, data, attribute, expected):
        """
        Tests given colour appearance model specification attribute value.

        Parameters
        ----------
        case : int
            Fixture case number.
        data : dict.
            Fixture case data.
        attribute : unicode.
            Tested attribute name.
        expected : float.
            Expected attribute value.

        Returns
        -------
        None
        """

        specification = self.get_output_specification_from_data(data)
        value = specification[attribute]

        error_message = (
            'Parameter "{0}" in test case "{1}" does not match target value.\n'
            'Expected: "{2}" \n'
            'Received "{3}"').format(attribute, case, expected, value)

        assert_allclose(value,
                        expected,
                        err_msg=error_message,
                        rtol=0.01,
                        atol=0.01,
                        verbose=False)

        assert_almost_equal(value,
                            expected,
                            decimal=1,
                            err_msg=error_message)

