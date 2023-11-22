import os
import time
from itertools import product

import pandas as pd

from Module.utility.len_time_module import time_convert, basepair_convert
from Module.utility.wait_display import progress


def count_kmers(Sequence, kmer, kmin, kmax):
    n = len(Sequence)
    km = range(kmin, kmax + 1)
    counter = dict()
    disp = 0
    for k in km:
        per = (n - k) // 50
        for i in range(0, n - k + 1, 1):
            mer = Sequence[i: i + k]
            counter[mer] = counter.get(mer, 0) + 1
            disp += 1
            if disp % per == 0:
                progress(disp // per)
    return [counter.get(key, 0) for key in kmer]


def generate_kmer(m, n):
    kmer = []
    for k in range(m, n + 1):
        kmer.extend(["".join(i) for i in product('ATGC', repeat=k)][-2000:])
    return kmer


# noinspection PyGlobalUndefined
def sequence2kmer(seq_path: str) -> str:
    """
    The function takes a sequence file as input and generates kmers of length 6 and 7 (last 2000 each)
    for more info. refer the sample features csv file
    :param seq_path: Path to the sequence fasta file.
    :return: Last 2000 kmers of length 6 and 7 as a csv file.
    """

    m = 6
    n = 7

    kmer = generate_kmer(m, n)

    dir_name = os.path.dirname(os.path.dirname(seq_path))
    fname = os.path.splitext(os.path.basename(seq_path))[0]
    # print(dir_name)
    feature_dir = os.path.join(dir_name, "Features")
    # print(feature_dir)
    if not os.path.exists(feature_dir):
        os.mkdir(feature_dir)

    df = pd.DataFrame(columns=kmer)
    filenames = []
    tstamp = []
    filesize = []

    time1 = time.perf_counter()
    with open(seq_path, 'r') as seq_file:
        sequence = seq_file.read()

    bsp = basepair_convert(len(sequence))
    filenames.append(fname)
    filesize.append(bsp)
    print("--" * 35)
    print(f"Generating Features.")
    df.loc[len(df)] = count_kmers(sequence, kmer, m, n)
    time2 = time.perf_counter()
    print()
    print(f"Saving Generated Features.")
    tot_time = round(time2 - time1)
    print(f'Time Taken for Feature Generation [HH:MM:SS]: {time_convert(tot_time)}')
    print()
    tstamp.append(time_convert(tot_time))
    df.columns = kmer
    feat_name = f'{fname}_features.csv'
    df.insert(0, "Filename", filenames, True)
    df.insert(1, "BasePairs", filesize, True)
    df.insert(2, "ProcessingTime", tstamp, True)
    file_path = os.path.join(feature_dir, feat_name)
    df.to_csv(file_path, index=False)

    return file_path
