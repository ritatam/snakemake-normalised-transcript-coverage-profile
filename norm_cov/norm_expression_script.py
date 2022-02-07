import os
import argparse

def main():
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(dest="command")
    
    bed_file_split_parser = subparsers.add_parser("refbedsplit", help="Splits reference genome window bed file into even chunks to allow for parallelisation.")
    bed_file_split_parser.add_argument("--bed", metavar="", required=True, help="Abspath to reference genome window bed file.")
    bed_file_split_parser.add_argument("--chunks", type=int, metavar="", required=True, help="Number of chunks the bed file is split into (# of threads).")
    bed_file_split_parser.add_argument("--tmp_path", metavar="", required=True, help="Abspath to temporary directory where ref genome bed chunk files are saved.")
    bed_file_split_parser.set_defaults(func=bed_file_split)
    
    args = parser.parse_args()
    if args.command == "refbedsplit":
        bed_file_split(args.bed, args.chunks, args.tmp_path)



def bed_file_split(bed_fn, num_chunks, tmp_path):
    '''
    Splits a bed file into even chunks and outputs each as temporary file.
    Each file has the same number of lines, except the last chunk which covers the last bit of contigs.
    Returns a list of split bed file abspaths in tmp_path.
    '''
    if not os.path.exists(tmp_path):
        os.makedirs(tmp_path)
        print(f"\nTemporary directory created at {tmp_path}\n")
    
    num_lines = 0
    with open(bed_fn, 'rb') as bed:
        for line in bed:
            num_lines += 1
    print(f'Number of lines in bedfile: {num_lines}')
    chunk_size = num_lines//num_chunks
    print(f'Target chunk size: {chunk_size}')
    
    # chop bed window file into chunks for parallel computing
    previous = 0
    files = []
    for i, chunk in enumerate([x for x in range(0, num_lines,chunk_size)]):
        if chunk == 0:
            continue
        else:
            temp_fn = os.path.join(tmp_path, f'{os.path.basename(bed_fn)}_chunk_{i-1}')
            with open(temp_fn, 'w') as temp_file:
                with open(bed_fn, 'r') as bed:
                    for line_num, line in enumerate(bed):
                        if line_num < chunk and line_num >= previous:
                            print(line.rstrip(), file=temp_file)
            previous = chunk
            files.append(temp_fn)
            
    # chunk covering the last window
    if chunk < num_lines:
        temp_fn = os.path.join(tmp_path, f'{os.path.basename(bed_fn)}_chunk_{i}')
        with open(temp_fn, 'w') as temp_file:
            with open(bed_fn, 'r') as bed:
                for line_num, line in enumerate(bed):
                    if line_num >= chunk:
                        print(line.rstrip(), file=temp_file)
    files.append(temp_fn)
    print("\nBed file split into chunks!\n")
    return len(files)-1


if __name__ == "__main__":
    main()