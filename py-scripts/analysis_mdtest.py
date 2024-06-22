import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from utils.prepare_data import load_and_prepare_data

df = load_and_prepare_data('data/df_mdtest.csv', is_cosbench=False)

sns.set_style('whitegrid')

# Filter operations and systems
operations = df[df['Operation'].isin([
    'Directory creation', 'Directory stat', 'Directory rename', 'Directory removal',
    'File creation', 'File stat', 'File read', 'File removal'
])]['Operation'].unique()
systems = df['System'].unique()

fig, ax = plt.subplots(figsize=(14, 7))
colors = {'CEPH': '#1f77b4', 'Lustre': '#2ca02c', 'JuiceFS': '#ff7f0e'}
bar_width = 0.2

# Plot bar charts
for i, operation in enumerate(operations):
    for j, system in enumerate(systems):
        mean_value = df[(df['Operation'] == operation) & (df['System'] == system)]['Mean'].values[0]
        label = f'{operation} - {system}' if 'Directory' not in operation else f'{operation.split()[1]} - {system}'
        ax.bar(i + j * bar_width, mean_value, bar_width, label=label, color=colors[system])

ax.set_xticks(np.arange(len(operations)) + (len(systems) - 1) * bar_width / 2)
ax.set_xticklabels([op.replace("Directory ", "Dir ") for op in operations], fontsize=18, rotation=45, ha='right')
ax.set_ylabel('Mean Time (ms)', fontsize=18, labelpad=15)

# Add legend
handles = [plt.Rectangle((0, 0), 1, 1, color=colors[system]) for system in systems]
ax.legend(handles, systems, loc='upper right', fontsize=18)

ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
plt.tick_params(axis='both', which='major', labelsize=18)

plt.tight_layout()

# Save plot as EPS file
plt.savefig('output/fig5.eps', format='eps')

plt.show()
