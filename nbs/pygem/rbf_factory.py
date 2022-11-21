"""
Factory class for radial basis functions
"""
import numpy as np


class classproperty(object):
    def __init__(self, f):
        self.f = f

    def __get__(self, obj, owner):
        return self.f(owner)


class RBFFactory(object):
    """
    Factory class that spawns the radial basis functions.

    :Example:
        
        >>> from pygem import RBFFactory
        >>> import numpy as np
        >>> x = np.linspace(0, 1)
        >>> for fname in RBFFactory.bases:
        >>>     y = RBFFactory(fname)(x)
    """
    def gaussian_spline(X, r=1):
        """
        It implements the following formula:

        .. math::
            \\varphi(\\boldsymbol{x}) = e^{-\\frac{\\boldsymbol{x}^2}{r^2}}

        :param numpy.ndarray X: the norm x in the formula above.
        :param float r: the parameter r in the formula above.

        :return: result: the result of the formula above.
        :rtype: float
        """
        result = np.exp(-(X * X) / (r * r))
        return result

    def multi_quadratic_biharmonic_spline(X, r=1):
        """
        It implements the following formula:

        .. math::
            \\varphi(\\boldsymbol{x}) = \\sqrt{\\boldsymbol{x}^2 + r^2}

        :param numpy.ndarray X: the norm x in the formula above.
        :param float r: the parameter r in the formula above.

        :return: result: the result of the formula above.
        :rtype: float
        """
        result = np.sqrt((X * X) + (r * r))
        return result

    def inv_multi_quadratic_biharmonic_spline(X, r=1):
        """
        It implements the following formula:

        .. math::
            \\varphi(\\boldsymbol{x}) =
            (\\boldsymbol{x}^2 + r^2 )^{-\\frac{1}{2}}

        :param numpy.ndarray X: the norm x in the formula above.
        :param float r: the parameter r in the formula above.

        :return: result: the result of the formula above.
        :rtype: float
        """
        result = 1.0 / (np.sqrt((X * X) + (r * r)))
        return result

    def thin_plate_spline(X, r=1):
        """
        It implements the following formula:

        .. math::
            \\varphi(\\boldsymbol{x}) =
            \\left(\\frac{\\boldsymbol{x}}{r}\\right)^2
            \\ln\\frac{\\boldsymbol{x}}{r}

        :param numpy.ndarray X: the norm x in the formula above.
        :param float r: the parameter r in the formula above.

        :return: result: the result of the formula above.
        :rtype: float
        """
        arg = X / r
        result = arg * arg
        result = np.where(arg > 0, result * np.log(arg), result)
        return result

    def beckert_wendland_c2_basis(X, r=1):
        """
        It implements the following formula:

        .. math::
            \\varphi(\\boldsymbol{x}) = 
            \\left( 1 - \\frac{\\boldsymbol{x}}{r}\\right)^4 +
            \\left( 4 \\frac{ \\boldsymbol{x} }{r} + 1 \\right)

        :param numpy.ndarray X: the norm x in the formula above.
        :param float r: the parameter r in the formula above.

        :return: result: the result of the formula above.
        :rtype: float
        """
        arg = X / r
        first = np.where((1 - arg) > 0, np.power((1 - arg), 4), 0)
        second = (4 * arg) + 1
        result = first * second
        return result

    def polyharmonic_spline(X, r=1, k=2):
        """
        It implements the following formula:

        .. math::
            
            \\varphi(\\boldsymbol{x}) =
                \\begin{cases}
                \\frac{\\boldsymbol{x}}{r}^k
                    \\quad & \\text{if}~k = 1,3,5,...\\\\
                \\frac{\\boldsymbol{x}}{r}^{k-1}
                \\ln(\\frac{\\boldsymbol{x}}{r}^
                {\\frac{\\boldsymbol{x}}{r}})
                    \\quad & \\text{if}~\\frac{\\boldsymbol{x}}{r} < 1,
                    ~k = 2,4,6,...\\\\
                \\frac{\\boldsymbol{x}}{r}^k
                \\ln(\\frac{\\boldsymbol{x}}{r})
                    \\quad & \\text{if}~\\frac{\\boldsymbol{x}}{r} \\ge 1,
                    ~k = 2,4,6,...\\\\
                \\end{cases}

        :param numpy.ndarray X: the norm x in the formula above.
        :param float r: the parameter r in the formula above.

        :return: result: the result of the formula above.
        :rtype: float
        """

        r_sc = X / r

        # k odd
        if k & 1:
            return np.power(r_sc, k)

        # k even
        result = np.where(r_sc < 1,
                          np.power(r_sc, k - 1) * np.log(np.power(r_sc, r_sc)),
                          np.power(r_sc, k) * np.log(r_sc))
        return result

    ############################################################################
    ##                                                                        ##
    ## BASIS FUNCTION dictionary                                              ##
    ##                                                                        ##
    ## New implementation must be added here.                                 ##
    ##                                                                        ##
    ############################################################################
    __bases = {
        'gaussian_spline': gaussian_spline,
        'multi_quadratic_biharmonic_spline': multi_quadratic_biharmonic_spline,
        'inv_multi_quadratic_biharmonic_spline':
        inv_multi_quadratic_biharmonic_spline,
        'thin_plate_spline': thin_plate_spline,
        'beckert_wendland_c2_basis': beckert_wendland_c2_basis,
        'polyharmonic_spline': polyharmonic_spline
    }

    def __new__(self, fname):

        # to make the str callable we have to use a dictionary with all the
        # implemented radial basis functions
        if fname in self.bases:
            return self.__bases[fname]
        else:
            raise NameError(
                """The name of the basis function in the parameters file is not
                correct or not implemented. Check the documentation for
                all the available functions.""")

    @classproperty
    def bases(self):
        """
        The available basis functions.
        """
        return list(self.__bases.keys())
