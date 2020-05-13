import numpy as np
import textwrap


def proximate_analysis(fc, vm, ash, moisture, disp=False):
    """
    Convert proximate analysis from as-received basis to dry and dry-ash free
    bases.

    Parameters
    ----------
    fc : float
        Percent fixed carbon
    vm : float
        Percent volatile matter
    ash : float
        Percent ash
    moisture : float
        Percent moisture
    disp : bool, optional
        Print results to console, default is `False`

    Returns
    -------
    proximate_bases : dict
        Proximate analysis bases calculated from as-received basis. Keys and
        associated list of values in the dictionary are

        - `'ar': [fc, vm, ash, moisture]` for as-received basis (% ar)
        - `'dry': [fc, vm, ash]` for dry basis (% dry)
        - `'daf': [fc, vm]` for dry ash-free basis (% daf)

        where `fc` is fixed carbon and `vm` is volatile matter.

    Raises
    ------
    ValueError
        If the proximate analysis sum is not 100.

    Example
    -------
    >>> proximate_analysis(16.92, 76.40, 0.64, 6.04)
    {
        'ar': [16.92, 76.4, 0.64, 6.04],
        'dry': [18.00, 81.31, 0.68],
        'daf': [18.13, 81.86]
    }
    """

    # as-received basis (% ar)
    prox_ar = [fc, vm, ash, moisture]
    sum_ar = sum(prox_ar)

    # make sure proximate analysis sums to 100
    if not np.isclose(sum_ar, 100.0):
        raise ValueError('Sum of proximate analysis values must be 100')

    # dry basis (% dry)
    prox_dry = [100 * x / (sum_ar - prox_ar[-1]) for x in prox_ar[:-1]]
    sum_dry = sum(prox_dry)

    # dry ash-free basis (% daf)
    prox_daf = [100 * x / (sum_dry - prox_dry[-1]) for x in prox_dry[:-1]]
    sum_daf = sum(prox_daf)

    # results dictionary
    proximate_bases = {
        'ar': prox_ar,
        'dry': prox_dry,
        'daf': prox_daf
    }

    # print results to console if `disp=True`
    if disp:
        results = textwrap.dedent(f"""
                        % ar    % dry    % daf
        FC          {prox_ar[0]:8} {prox_dry[0]:8.2f} {prox_daf[0]:8.2f}
        VM          {prox_ar[1]:8} {prox_dry[1]:8.2f} {prox_daf[1]:8.2f}
        ash         {prox_ar[2]:8} {prox_dry[2]:8.2f}
        moisture    {prox_ar[3]:8}
        sum         {sum_ar:8.2f} {sum_dry:8.2f} {sum_daf:8.2f}
        """)
        print(results)

    return proximate_bases
