import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from utils.prepare_data import load_and_prepare_data

df = load_and_prepare_data('data/df_cosbench_write.csv')

sns.set_style('whitegrid')

# Plotting
plt.figure(figsize=(14, 7))
unique_sizes = df['Size_KB'].unique()
markers = ['o', 's', 'D', '^', 'v', '<', '>']
palette = sns.color_palette()

# Plot each storage type and object size
for i, storage in enumerate(df['Storage'].unique()):
    for j, size in enumerate(unique_sizes):
        subset = df[(df['Storage'] == storage) & (df['Size_KB'] == size)]
        if not subset.empty:
            label = f'{storage}, {size//1024 if size >= 1024 else size} {"MB" if size >= 1024 else "KB"}'
            plt.plot(subset['Throughput'], subset['Avg-ResTime'],
                     label=label, marker=markers[j % len(markers)], linestyle='-', color=palette[i])

plt.xlabel('Throughput (op/s)', fontsize=18, labelpad=15)
plt.ylabel('Average Response Time (ms)', fontsize=18, labelpad=15)
plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left', fontsize=18)
plt.grid(True)
for spine in ['top', 'right', 'left', 'bottom']:
    plt.gca().spines[spine].set_visible(False)
plt.tick_params(axis='both', which='major', labelsize=18)

plt.tight_layout()

# Save plot as EPS file
plt.savefig('output/fig4.eps', format='eps')

plt.show()
