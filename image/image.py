"""
This module holds classes related to images.
A strong focus is given to ITK images and numpy arrays.
"""
import SimpleITK as sitk


class ImageProperties:
    """
    Represents ITK image properties.
    Also refer to itk::simple::Image::CopyInformation.
    """

    def __init__(self, image: sitk.Image):
        """
        Initializes a new instance of the ImageInformation class.
        :param image: The image.
        """
        self.size = image.GetSize()
        self.origin = image.GetOrigin()
        self.spacing = image.GetSpacing()
        self.direction = image.GetDirection()
        self.dimensions = image.GetDimension()
        self.number_of_components_per_pixel = image.GetNumberOfComponentsPerPixel()

    def is_two_dimensional(self) -> bool:
        """
        Determines whether the image is two-dimensional.
        :return: True if the image is two-dimensional; otherwise, False.
        :rtype: bool
        """
        return self.dimensions == 2

    def is_three_dimensional(self) -> bool:
        """
        Determines whether the image is three-dimensional.
        :return: True if the image is three-dimensional; otherwise, False.
        :rtype: bool
        """
        return self.dimensions == 3

    def is_vector_image(self) -> bool:
        """
        Determines whether the image is a vector image.
        :return: True for vector images; False for scalar images.
        :rtype: bool
        """
        return self.number_of_components_per_pixel > 1

    def __str__(self):
        """
        Gets a nicely printable string representation.
        :return: String representation.
        :rtype: str
        """
        return 'ImageProperties:\n' \
               ' size:                           {self.size}\n' \
               ' origin:                         {self.origin}\n' \
               ' spacing:                        {self.spacing}\n' \
               ' direction:                      {self.direction}\n' \
               ' dimensions:                     {self.dimensions}\n' \
               ' number_of_components_per_pixel: {self.number_of_components_per_pixel}\n' \
            .format(self=self)


class NumpySimpleITKImageBridge:
    """
    Represents a numpy to SimpleITK bridge.
    It provides static methods to convert between numpy array and SimpleITK image.
    """

    @staticmethod
    def array_to_image(array, information: ImageProperties) -> sitk.Image:
        """
        Converts a one-dimensional numpy array to a SimpleITK image.
        :param array: The image as numpy one-dimensional array, e.g. shape=(n,), where n = total number of voxels.
        :param information: The image information.
        :return: The SimpleITK image. 
        """

        if array.ndim != 1:
            raise ValueError("array needs to be one-dimensional")

        array = array.reshape((information.size[2], information.size[1], information.size[0]))

        image = sitk.GetImageFromArray(array)
        image.SetOrigin(information.origin)
        image.SetSpacing(information.spacing)
        image.SetDirection(information.direction)

        return image

    @staticmethod
    def array_to_vector_image(array, information: ImageProperties) -> sitk.Image:
        """
        Converts a two-dimensional numpy array to a SimpleITK vector image.
        :param array: The image as numpy two-dimensional array, e.g. shape=(4181760,2).
        :param information: The image information.
        :return: The SimpleITK image. 
        """

        if array.ndim != 2:
            raise ValueError("array needs to be two-dimensional")

        array = array.reshape((information.size[2], information.size[1], information.size[0], array.shape[1]))

        image = sitk.GetImageFromArray(array)
        image.SetOrigin(information.origin)
        image.SetSpacing(information.spacing)
        image.SetDirection(information.direction)

        return image


class SimpleITKNumpyImageBridge:
    """
    Represents a SimpleITK to numpy bridge.
    It provides static methods to convert between SimpleITK image and numpy array.
    """

    @staticmethod
    def convert(image: sitk.Image):
        """
        Converts 
        :param image: The image. 
        :return: (array, info): The image as numpy array and the ImageProperties.
        """

        return sitk.GetArrayFromImage(image), ImageProperties(image)
