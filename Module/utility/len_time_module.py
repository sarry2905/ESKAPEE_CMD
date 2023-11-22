import datetime
import hurry.filesize as hf


def basepair_convert(seqlen):
    """
    :param seqlen: Length of the sequence
    :return: modified representation of basepair for display
    """
    return hf.size(seqlen, system=hf.si)


def time_convert(n):
    return str(datetime.timedelta(seconds=n))


def time_estimate(bspair):
    val = float(bspair[:-1])
    sz = bspair[-1]
    if sz == 'K':
        mx = 1
        mn = 0.5
        val = val / 1000
    elif sz == 'M':
        if val < 100.0:
            mx = 1.34
            mn = 1.08
        else:
            mx = 1.23
            mn = 1.05
    elif sz == 'G':
        mx = 1.48
        mn = 1.34
        val = val * 1000
    else:
        print(f'Error___Estimate Time cant be calculated for the {bspair} BasePairs')
        return
    mxtm = int(mx * val)
    mntm = int(mn * val)
    return [mntm, mxtm]
