import glob
import os

import time
import traceback

import pandas as pd
from prettytable import PrettyTable as Ptbl
from pathlib import Path

from Module.classify import eskapee_classification
from Module.sequence_process import extract_sequence
from Module.feature_generation import sequence2kmer
from Module.utility.len_time_module import time_estimate, time_convert, basepair_convert


def process_gzip(folder):
    path = folder + "/*.gz"
    file_path = glob.glob(path)
    return file_path


def process_fastq(folder):
    path = folder + "/*.fastq"
    file_path = glob.glob(path)
    return file_path


def feature_file_path(file_path):
    file_name = os.path.splitext(os.path.basename(file_path))[0]
    dir_name = os.path.dirname(os.path.dirname(file_path))
    featuredir = os.path.join(dir_name, "Features")
    # feat_file = os.path.splitext(file_name)[0] + "_features.csv"
    feat_file = file_name + "_features.csv"
    feat_path = os.path.join(featuredir, feat_file)
    return feat_path


# noinspection PyGlobalUndefined
def main(args):
    global fname
    result = None
    final_table = None
    # final_result = {}
    files = []

    if args.Folder is not None:
        files.extend(process_gzip(args.Folder))
        if len(files) > 1:
            print("--" * 37)
            print(f"Input path contains {len(files)} .gz files")
        elif len(files) == 1:
            print("--" * 37)
            print(f"Input path contains only 1 .gz file")
        else:
            print("--" * 37)
            print(f"The given path does not contain any .gz files!!")
            print("TERMINATING....")
            exit(0)
    elif args.gzfile is not None:
        ftype = os.path.splitext(args.gzfile)[1]
        if ftype == '.gz':
            files.append(args.gzfile)
            print("--" * 37)
            print("Only 1 file to be processed")
        else:
            print(f"Invalid File Format\nExpected Format: .gz")
            exit(0)
    else:
        print()
        print("--" * 37)
        print("Please provide Input through a .gz file or a folder containing multiple gz files")
        exit(0)

    multi_data = True if len(files) > 1 else False

    if multi_data:
        final_table = Ptbl(field_names=('Filename', 'ESKAPEE/Non-ESKAPEE', 'Subclass','Status'))

    cls_dir = Path.cwd().joinpath('Data/classification')
    cls_dir.mkdir(parents=True, exist_ok=True)

    for gzpath in files:
        gzfile = os.path.splitext(os.path.basename(gzpath))[0]
        try:
            seq_info = extract_sequence(gzpath)
            if seq_info is not None:
                seq_path = seq_info['path']
                seq_len = seq_info['len']
                fname = os.path.splitext(os.path.basename(seq_path))[0]
                bsp = basepair_convert(seq_len)
                time_est = time_estimate(bsp)
                print(f"# of Base Pairs: {bsp}")

                feature_path = feature_file_path(seq_path)
                if os.path.exists(feature_path):
                    print(f"** Feature File for {fname} already exists in the database **")
                    print("Proceeding with the Classification Step")
                    time.sleep(1)
                    data = pd.read_csv(feature_path)
                else:
                    print('Estimated Time for Feature Generation & Classification [HH:MM:SS]')
                    print(f'Minimum Time: {time_convert(time_est[0])}')
                    print(f'Maximum Time: {time_convert(time_est[1])}')

                    csvfile = sequence2kmer(seq_path)
                    print(f"Features saved in {csvfile} ")
                    data = pd.read_csv(csvfile)
                    print("--" * 37)
                    time.sleep(2)

                cls_df = data.iloc[:, :3].copy()
                cls_df['MainClass']=''
                cls_df['SubClass']=''
                cls_df['Status']=''
                result = eskapee_classification(data)
                result['status'] = 'SUCCESS'
                result['Filename'] = gzfile
            else:
                print("[[ ERROR INFO ]] File does not have any data, it might be corrupt.. Please recheck!!!")
                result = {
                    'Filename': gzfile,
                    'mncl': '-',
                    'sbcl': '-',
                    'status': 'ERROR'
                        }
        except TypeError as te:
            print("There is a data type mismatch in writing to the file. Please check this file again")
            print(te)
            result = {
                'Filename': gzfile,
                'mncl': '-',
                'sbcl': '-',
                'status': f'ERROR {te}'
            }
        except IOError as ie:
            print("There was problem reading the file from the given path. Please check the path for this file again")
            print(ie)
            result = {
                'Filename': gzfile,
                'mncl': '-',
                'sbcl': '-',
                'status': f'ERROR {ie}'
            }
        except EOFError as eoe:
            print("There was End of File error. The file might be corrupt. Check this file again")
            print(eoe)
            result = {
                'Filename': gzfile,
                'mncl': '-',
                'sbcl': '-',
                'status': f'ERROR {eoe}'
            }
        except Exception as e:
            print(traceback.format_exc())
            print("Error in one of the modules maybe")
            print(e)
            result = {
                'Filename': gzfile,
                'mncl': '-',
                'sbcl': '-',
                'status': f'ERROR {e}'
            }
        res_table = Ptbl(field_names=['Filename', 'ESKAPEE/Non-ESKAPEE', 'Subclass', 'Status'])
        res_table.min_table_width = 100
        res_table.align = 'c'

        res_table.add_row([result['Filename'],result['mncl'],result['sbcl'],result['status']])
        print("=~" * 15, end='')
        print(" Prediction Results ", end='')
        print("=~" * 15)
        print(res_table)
        clsf = f"{cls_df.loc[0, 'Filename']}_Output.csv"
        clsfname = os.path.join(cls_dir, clsf)
        cls_df.loc[0, 'MainClass'] = result['mncl']
        cls_df.loc[0, 'SubClass'] = result['sbcl']
        cls_df.loc[0, 'Status'] = result['status']
        cls_df.to_csv(clsfname, index=False)

        if multi_data:
            final_table.add_row([result['Filename'],result['mncl'],result['sbcl'],result['status']])

    if multi_data:
        print()
        print()
        print("~~" * 12, end='')
        print("Prediction Results Summary for all input files", end='')
        print("~~" * 12)
        print(final_table)
        print()
        print()


print("Completed")
