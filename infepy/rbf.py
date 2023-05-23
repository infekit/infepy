# AUTOGENERATED! DO NOT EDIT! File to edit: ../nbs/4_rbf.ipynb.

# %% auto 0
__all__ = ['RBF']

# %% ../nbs/4_rbf.ipynb 3
import os
import numpy as np
from nbdev.showdoc import *
import matplotlib.pyplot as plt
from scipy.spatial.distance import cdist

# %% ../nbs/4_rbf.ipynb 4
from .deformation import Deformation
from .rbf_factory import RBFFactory

# %% ../nbs/4_rbf.ipynb 5
try:
    import configparser as configparser
except ImportError:
    import ConfigParser as configparser

# %% ../nbs/4_rbf.ipynb 9
class RBF(Deformation):
    """
    Class that handles the Radial Basis Functions interpolation on the mesh points"""

    def __init__(
        self,
        original_control_points=None,  # (*n_control_points*, *3*) array with the coordinates of the original interpolation control points before the deformation. *Default is the vertices of the unit cube.*
        deformed_control_points=None,  # (*n_control_points*, *3*) array with the coordinates of the interpolation control points after the deformation. *Default is the vertices of the unit cube.*
        func="thin_plate_spline",  # MODIFIED: DEFAULT is **thin plate spline**. Several basis function are already implemented and they are available through the `~pygem.rbf.RBF` by passing the name of the right function.
        radius=1,  # Scaling parameter that affects the shape of the basis functions.
        smoothing=None,  # MODIFIED: added parameter. IF defined, a constant values will be added on the diagonal of the matrix Dcc. s
        extra_parameter=None,
    ):
        self.basis = func
        self.radius = radius
        self.smoothing = smoothing

        if original_control_points is None:
            self.original_control_points = np.array(
                [
                    [0.0, 0.0, 0.0],
                    [0.0, 0.0, 1.0],
                    [0.0, 1.0, 0.0],
                    [1.0, 0.0, 0.0],
                    [0.0, 1.0, 1.0],
                    [1.0, 0.0, 1.0],
                    [1.0, 1.0, 0.0],
                    [1.0, 1.0, 1.0],
                ]
            )
        else:
            self.original_control_points = original_control_points

        if deformed_control_points is None:
            self.deformed_control_points = np.array(
                [
                    [0.0, 0.0, 0.0],
                    [0.0, 0.0, 1.0],
                    [0.0, 1.0, 0.0],
                    [1.0, 0.0, 0.0],
                    [0.0, 1.0, 1.0],
                    [1.0, 0.0, 1.0],
                    [1.0, 1.0, 0.0],
                    [1.0, 1.0, 1.0],
                ]
            )
        else:
            self.deformed_control_points = deformed_control_points

        self.extra = extra_parameter if extra_parameter else dict()

        self.weights = self._get_weights(
            self.original_control_points, self.deformed_control_points
        )

    @property
    def n_control_points(self):
        """
        Total number of control points.

        :rtype: int
        """
        return self.original_control_points.shape[0]

    @property
    def basis(self):
        """
        The kernel to use in the deformation.

        :getter: Returns the callable kernel
        :setter: Sets the kernel. It is possible to pass the name of the
            function (check the list of all implemented functions in the
            `pygem.rbf_factory.RBFFactory` class) or directly the callable
            function.
        :type: callable
        """
        return self.__basis

    @basis.setter
    def basis(self, func):
        if callable(func):
            self.__basis = func
        elif isinstance(func, str):
            self.__basis = RBFFactory(func)
        else:
            raise TypeError("`func` is not valid.")

    def _get_weights(self, X, Y):
        """
        This private method, given the original control points and the deformed
        ones, returns the matrix with the weights and the polynomial terms, that
        is :math:`W`, :math:`c^T` and :math:`Q^T`. The shape is
        (*n_control_points+1+3*, *3*).

        :param numpy.ndarray X: it is an n_control_points-by-3 array with the
            coordinates of the original interpolation control points before the
            deformation.
        :param numpy.ndarray Y: it is an n_control_points-by-3 array with the
            coordinates of the interpolation control points after the
            deformation.

        :return: weights: the 2D array with the weights and the polynomial terms.
        :rtype: numpy.ndarray
        """
        npts, dim = X.shape
        H = np.zeros((npts + 3 + 1, npts + 3 + 1))
        H[:npts, :npts] = self.basis(cdist(X, X), self.radius)
        H[npts, :npts] = 1.0
        H[:npts, npts] = 1.0
        H[:npts, -3:] = X
        H[-3:, :npts] = X.T
        if (
            self.smoothing
        ):  # MODIFIED: smoothing add a constant values along the Dcc Matrix. Read more into the paper from Forti and Rozza for the H structure.
            np.fill_diagonal(H[:npts, :npts], self.smoothing)

        rhs = np.zeros((npts + 3 + 1, dim))
        rhs[:npts, :] = Y
        weights = np.linalg.solve(H, rhs)
        return weights

    def read_parameters(self, filename="parameters_rbf.prm"):
        """
        Reads in the parameters file and fill the self structure.

        :param string filename: parameters file to be read in. Default value is
            parameters_rbf.prm.
        """
        if not isinstance(filename, str):
            raise TypeError("filename must be a string")

        # Checks if the parameters file exists. If not it writes the default
        # class into filename.  It consists in the vetices of a cube of side one
        # with a vertex in (0, 0, 0) and opposite one in (1, 1, 1).
        if not os.path.isfile(filename):
            self.write_parameters(filename)
            return

        config = configparser.RawConfigParser()
        config.read(filename)

        self.basis = config.get("Radial Basis Functions", "basis function")
        self.radius = config.getfloat("Radial Basis Functions", "radius")

        ctrl_points = config.get("Control points", "original control points")
        lines = ctrl_points.split("\n")
        original_control_points = np.zeros((len(lines), 3))
        for line, i in zip(lines, list(range(0, self.n_control_points))):
            values = line.split()
            original_control_points[i] = np.array(
                [float(values[0]), float(values[1]), float(values[2])]
            )
        self.original_control_points = original_control_points

        mod_points = config.get("Control points", "deformed control points")
        lines = mod_points.split("\n")

        if len(lines) != self.n_control_points:
            raise TypeError(
                "The number of control points must be equal both in"
                "the 'original control points' and in the 'deformed"
                "control points' section of the parameters file"
                "({0!s})".format(filename)
            )

        deformed_control_points = np.zeros((self.n_control_points, 3))
        for line, i in zip(lines, list(range(0, self.n_control_points))):
            values = line.split()
            deformed_control_points[i] = np.array(
                [float(values[0]), float(values[1]), float(values[2])]
            )
        self.deformed_control_points = deformed_control_points

    def write_parameters(self, filename="parameters_rbf.prm"):
        """
        This method writes a parameters file (.prm) called `filename` and fills
        it with all the parameters class members. Default value is
        parameters_rbf.prm.

        :param string filename: parameters file to be written out.
        """
        if not isinstance(filename, str):
            raise TypeError("filename must be a string")

        output_string = ""
        output_string += "\n[Radial Basis Functions]\n"
        output_string += "# This section describes the radial basis functions"
        output_string += " shape.\n"

        output_string += "\n# basis funtion is the name of the basis functions"
        output_string += " to use in the transformation. The functions\n"
        output_string += "# implemented so far are: gaussian_spline,"
        output_string += " multi_quadratic_biharmonic_spline,\n"
        output_string += "# inv_multi_quadratic_biharmonic_spline,"
        output_string += " thin_plate_spline, beckert_wendland_c2_basis,"
        output_string += " polyharmonic_spline.\n"
        output_string += "# For a comprehensive list with details see the"
        output_string += " class RBF.\n"
        output_string += "basis function: {}\n".format("gaussian_spline")

        output_string += "\n# radius is the scaling parameter r that affects"
        output_string += " the shape of the basis functions. See the"
        output_string += " documentation\n"
        output_string += "# of the class RBF for details.\n"
        output_string += "radius: {}\n".format(str(self.radius))

        output_string += "\n\n[Control points]\n"
        output_string += "# This section describes the RBF control points.\n"

        output_string += "\n# original control points collects the coordinates"
        output_string += " of the interpolation control points before the"
        output_string += " deformation.\n"

        output_string += "original control points:"
        offset = 1
        for i in range(0, self.n_control_points):
            output_string += (
                offset * " "
                + str(self.original_control_points[i][0])
                + "   "
                + str(self.original_control_points[i][1])
                + "   "
                + str(self.original_control_points[i][2])
                + "\n"
            )
            offset = 25

        output_string += "\n# deformed control points collects the coordinates"
        output_string += " of the interpolation control points after the"
        output_string += " deformation.\n"

        output_string += "deformed control points:"
        offset = 1
        for i in range(0, self.n_control_points):
            output_string += (
                offset * " "
                + str(self.deformed_control_points[i][0])
                + "   "
                + str(self.deformed_control_points[i][1])
                + "   "
                + str(self.deformed_control_points[i][2])
                + "\n"
            )
            offset = 25

        with open(filename, "w") as f:
            f.write(output_string)

    def __str__(self):
        """
        This method prints all the RBF parameters on the screen. Its purpose is
        for debugging.
        """
        string = ""
        string += "basis function = {}\n".format(self.basis)
        string += "radius = {}\n".format(self.radius)
        string += "\noriginal control points =\n"
        string += "{}\n".format(self.original_control_points)
        string += "\ndeformed control points =\n"
        string += "{}\n".format(self.deformed_control_points)
        return string

    def plot_points(self, filename=None):
        """
        Method to plot the control points. It is possible to save the resulting
        figure.

        :param str filename: if None the figure is shown, otherwise it is saved
            on the specified `filename`. Default is None.
        """
        fig = plt.figure(1)
        axes = fig.add_subplot(111, projection="3d")
        orig = axes.scatter(
            self.original_control_points[:, 0],
            self.original_control_points[:, 1],
            self.original_control_points[:, 2],
            c="blue",
            marker="o",
        )
        defor = axes.scatter(
            self.deformed_control_points[:, 0],
            self.deformed_control_points[:, 1],
            self.deformed_control_points[:, 2],
            c="red",
            marker="x",
        )

        axes.set_xlabel("X axis")
        axes.set_ylabel("Y axis")
        axes.set_zlabel("Z axis")

        plt.legend(
            (orig, defor),
            ("Original", "Deformed"),
            scatterpoints=1,
            loc="lower left",
            ncol=2,
            fontsize=10,
        )

        # Show the plot to the screen
        if filename is None:
            plt.show()
        else:
            fig.savefig(filename)

    def compute_weights(self):
        """
        This method compute the weights according to the
        `original_control_points` and `deformed_control_points` arrays.
        """
        self.weights = self._get_weights(
            self.original_control_points, self.deformed_control_points
        )

    def __call__(self, src_pts):
        """
        This method performs the deformation of the mesh points. After the
        execution it sets `self.modified_mesh_points`.
        """
        self.compute_weights()

        H = np.zeros((src_pts.shape[0], self.n_control_points + 3 + 1))
        H[:, : self.n_control_points] = self.basis(
            cdist(src_pts, self.original_control_points), self.radius
        )
        H[:, self.n_control_points] = 1.0
        H[:, -3:] = src_pts
        return np.asarray(np.dot(H, self.weights))
