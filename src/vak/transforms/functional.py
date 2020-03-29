import numpy as np
import torch

__all__ = [
    'pad_to_window',
    'reshape_to_window',
    'standardize_spect',
    'to_floattensor',
    'to_longtensor',
]


def standardize_spect(spect, mean_freqs, std_freqs, non_zero_std):
    """standardize spectrogram by subtracting off mean and dividing by standard deviation.

    Parameters
    ----------
    spect : numpy.ndarray
        with shape (frequencies, time bins)
    mean_freqs : numpy.ndarray
        vector of mean values for each frequency bin across the fit set of spectrograms
    std_freqs : numpy.ndarray
        vector of standard deviations for each frequency bin across the fit set of spectrograms
    non_zero_std : numpy.ndarray
        boolean, indicates where std_freqs has non-zero values. Used to avoid divide-by-zero errors.

    Returns
    -------
    transformed : numpy.ndarray
        with same shape as spect but with (approximately) zero mean and unit standard deviation
        (mean and standard devation will still vary by batch).
    """
    tfm = spect - mean_freqs[:, np.newaxis]  # need axis for broadcasting
    # keep any stds that are zero from causing NaNs
    tfm[non_zero_std, :] = tfm[non_zero_std, :] / std_freqs[non_zero_std, np.newaxis]
    return tfm


def pad_to_window(spect, window_size, padval=0., return_crop_vec=True):
    """pad a spectrogram so that it can be reshaped
    into consecutive windows of specified size

    Parameters
    ----------
    spect : numpy.ndarray
        with shape (frequencies, time bins)
    window_size : int
        number of time bins, i.e. columns in each window
        into which spectrogram will be divided.
    padval : float
        value to pad with. Added to "right side"
        of spectrogram.
    return_crop_vec : bool
        if True, return a boolean vector to use for cropping
        back down to size before padding. crop_vec has size
        equal to width of padded spectrogram, i.e. time bins
        plus padding on right side, and has values of 1 where
        columns in spect_padded are from the original spectrogram
        and values of 0 where columns were added for padding.

    Returns
    -------
    spect_padded : numpy.ndarray
        padded with padval
    crop_vec : np.bool
        has size equal to width of padded spectrogram, i.e. time bins
        plus padding on right side. Has values of 1 where
        columns in spect_padded are from the original spectrogram,
        and values of 0 where columns were added for padding.
        Only returned if return_crop_vec is True.
    """
    spect_height, spect_width = spect.shape
    target_width = int(
        np.ceil(spect_width / window_size) * window_size
    )
    spect_padded = np.ones((spect_height, target_width)) * padval
    spect_padded[:, :spect_width] = spect

    if return_crop_vec:
        crop_vec = np.zeros((target_width,), dtype=np.bool)
        crop_vec[:spect_width] = True
        return spect_padded, crop_vec
    else:
        return spect_padded


def reshape_to_window(spect, window_size):
    """resize a spectrogram into consecutive
    windows of specified size.

    Parameters
    ----------
    spect : numpy.ndarray
        with shape (frequencies, time bins)
    window_size

    Returns
    -------
    spect_windows
    """
    spect_height, spect_width = spect.shape
    return spect.reshape((-1, spect_height, window_size))


def to_floattensor(arr):
    """convert Numpy array to torch.FloatTensor.

    Parameters
    ----------
    arr : numpy.ndarray

    Returns
    -------
    float_tensor
        with dtype 'float32'
    """
    return torch.from_numpy(arr).float()


def to_longtensor(arr):
    """convert Numpy array to torch.LongTensor.

    Parameters
    ----------
    arr : numpy.ndarray

    Returns
    -------
    long_tensor : torch.Tensor
        with dtype 'float64'
    """
    return torch.from_numpy(arr).long()


def add_channel(input, channel_dim=0):
    """add a channel dimension to a 2-dimensional tensor.
    Transform that makes it easy to treat a spectrogram as an image,
    by adding a dimension with a single 'channel', analogous to grayscale.
    In this way the tensor can be fed to e.g. convolutional layers.

    Parameters
    ----------
    input : torch.Tensor
        with two dimensions (height, width).
    channel_dim : int
        dimension where "channel" is added.
        Default is 0, which returns a tensor with dimensions (channel, height, width).
    """
    if input.dim() != 2:
        raise ValueError(
            f'input tensor should have two dimensions but input.dim() is {input.dim()}'
        )
    return torch.unsqueeze(input, dim=channel_dim)
