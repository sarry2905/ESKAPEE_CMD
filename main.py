import argparse

from Module import genome


def main():
    parser = argparse.ArgumentParser(description="Sequence Preprocessing and Feature Generation (Kmer Count)")
    parser.add_argument("-F", "--Folder", help="Path of the Folder containing multiple files in .gz format")
    parser.add_argument("-i", "--gzfile", help="path to the Input fastq gz file")

    # args = parser.parse_args(["-F","E:\Genome_ICMR\Test_fastq\\"]) ##[-i,'E:\Genome_ICMR\Test_fastq\Ecol
    # i_part.fastq']) args = parser.parse_args(["-F","E:\Genome_Script_Server\Samples"])
    args = parser.parse_args()
    genome.main(args)


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    main()
