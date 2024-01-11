import csv
import statistics
import matplotlib.pyplot as plt
import sys


possible_candidates = []

def get_possible_candidates(fname, model_devi_f_trust_lo, model_devi_f_trust_hi,nEvery):
    row_count = 0 #number of atoms
    col_count = 0 #number of frame
    frameNum = []
    max_values = []
    results = []

    with open(fname, 'r') as csv_file:
        
        next(csv_file)

        for line in csv_file:
            row = list(map(float, line.strip().split()))
            row_count += 1
            col_count = len(row)-7
            values = row[7:] #skip the first 7 columns

            max_value = max(values)
            avg_value = statistics.mean(values)
            std_value = statistics.stdev(values)

            results.append([row[0], max_value, avg_value, std_value])
            frameNum.append(row[0])
            max_values.append(max_value)
        
        # plot histogram
        plt.figure()
        plt.hist(max_values, bins=50, edgecolor='k', alpha=0.7)
        plt.title('Histogram of Max Values')
        plt.xlabel('Max Error')
        plt.ylabel('Frequency')
        plt.grid(True, which='both', linestyle='--', linewidth=0.5)
        plt.tight_layout()
        plt.savefig('hist.pdf')

        print(max(max_values))
        plt.figure()
        plt.plot(max_values)
        plt.xlabel('Snapshot')
        plt.ylabel('Max Error')
        # plt.ylim((0,3))
        plt.tight_layout()
        plt.savefig('MaxOverTime.pdf')

        std_of_max_values = statistics.stdev(max_values)
        print(f'{std_of_max_values=}')
        avg_of_max_values = statistics.mean(max_values)
        print(f'{avg_of_max_values=}')
        first_frameNum = frameNum[0]
        print(f'First frame: {first_frameNum}')
        for i, r in enumerate(results):
            # based on model deviation force
            r[0] = r[0]-first_frameNum
            # skip first frame and only include nEvery
            if r[0]!=0 and r[0]%nEvery==0 and r[1] > model_devi_f_trust_lo and r[1] < model_devi_f_trust_hi: 
                possible_candidates.append(r[0])
    return possible_candidates



if __name__ == "__main__":
    
    model_devi_f_trust_lo = 0.05 # was 0.2
    model_devi_f_trust_hi = 0.15 # was 0.7
    sampleFreq = 10  # if lammps out_freq 10, timestep 5fs, then sampleFreq 100 is checking configs every 50fs
    modev_fname = sys.argv[1]

    candidates = get_possible_candidates(modev_fname, model_devi_f_trust_lo, model_devi_f_trust_hi,sampleFreq) 
    print(f'Possible candidates: {candidates}')
    print(f'Number of possible candidates: {len(candidates)}')