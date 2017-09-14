"""Utility functions for MNE."""
import numpy as np
import datetime
from ..utils import get_dsf

__all__ = ['mne_switch']


def mne_switch(file, ext, downsample, preload=True, **kwargs):
    """Read sleep datasets using mne.io.

    Parameters
    ----------
    file : string
        Filename (without extension).
    ext : string
        File extension (e.g. '.edf'').
    preload : bool | True
        Preload data in memory.
    kwargs : dict | {}
        Further arguments to pass to the mne.io.read function.

    Returns
    -------
    sf : float
        The original sampling-frequency.
    downsample : float
        The down-sampling frequency used.
    dsf : int
        The down-sampling factor.
    data : array_like
        The raw data of shape (n_channels, n_points)
    channels : list
        List of channel names.
    n : int
        Number of time points before down-sampling.
    start_time : datetime.time
        The time offset.
    """
    from mne import io

    # Get full path :
    path = file + ext

    # Preload :
    if preload is False:
        preload = 'temp.dat'
    kwargs['preload'] = preload

    if ext.lower() in ['.edf', '.bdf', '.gdf']:  # EDF / BDF / GDF
        raw = io.read_raw_edf(path, **kwargs)
    elif ext.lower == '.set':   # EEGLAB
        raw = io.read_raw_eeglab(path, **kwargs)
    elif ext.lower() == ['.egi', '.mff']:  # EGI / MFF
        raw = io.read_raw_egi(path, **kwargs)
    elif ext.lower() == '.cnt':  # CNT
        raw = io.read_raw_cnt(path, **kwargs)
    elif ext.lower() == '.vhdr':  # BrainVision
        raw = io.read_raw_brainvision(path, **kwargs)

    raw.pick_types(meg=True, eeg=True, ecg=True, emg=True)  # Remove stim lines
    sf = raw.info['sfreq']
    dsf, downsample = get_dsf(downsample, sf)
    channels = raw.info['ch_names']
    data = raw._data
    n = data.shape[1]
    start_time = datetime.time(0, 0, 0)  # raw.info['meas_date']
    anot = raw.annotations

    return sf, downsample, dsf, data[:, ::dsf], channels, n, start_time, anot
