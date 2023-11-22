import os
import gzip
from pathlib import Path


def readFastq(fh):  # function for reading and cleaning the raw clinical sequence.
    sequences = []  # It will store clean sequence.
    # with open(filename) as fh:  # opening clinical sequence
    while True:
        fh.readline()  # skip name line
        seq = fh.readline().rstrip()  # read base sequence
        fh.readline()  # skip placeholder line
        fh.readline()  # base quality line
        if len(seq) == 0:
            break
        sequences.append(seq)
    return sequences  # We want only clean sequence so returning only sequences.


def readFasta(fh):  # function for reading and cleaning the raw clinical sequence.
    sequences = []  # It will store clean sequence.
    # with open(filename) as fh:  # opening clinical sequence
    fh.readline()  # skip name line
    while True:
        seq = fh.readline().rstrip()  # read base sequence
        if len(seq) == 0:
            break
        sequences.append(seq)
    return sequences  # We want only clean sequence so returning only sequences.


def extract_sequence(gz_filepath):
    sequence_dir = Path.cwd().joinpath('Data/sequence')
    sequence_dir.mkdir(parents=True, exist_ok=True)
    fastq_formats = ['.fastq', '.fq']
    fasta_formats = ['.fasta', '.fna', '.ffn', '.faa', '.frn', '.fa']

    gz_file = os.path.basename(gz_filepath)
    fname = os.path.splitext(gz_file)[0]
    fileformat = os.path.splitext(fname)[1].lower()
    if fileformat not in fastq_formats and fileformat not in fasta_formats:
        print(f"Invalid File Format.. Sequence could not be extracted from {fileformat}  file.")
        return None

    seq_file = f'{fname.split(".")[0]}.txt'
    seq_path = os.path.join(sequence_dir, seq_file)
    print(f"Filename: {fname}")

    with gzip.open(gz_filepath, 'rt') as f_in:
        if fileformat in fastq_formats:
            sequence = ' '.join([str(element) for element in readFastq(f_in)]).replace(',', "").replace(" ", "")
        else:
            sequence = ' '.join([str(element) for element in readFasta(f_in)]).replace(',', "").replace(" ", "")

    with open(seq_path, 'w') as f_out:
        f_out.write(sequence)

    return {'path': seq_path, 'len': len(sequence)}
