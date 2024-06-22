import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from sklearn.linear_model import LinearRegression
from utils.prepare_data import load_and_prepare_data

df = load_and_prepare_data('data/data/df_cosbench_write.csv')

# Split data by storage type
storages = ['CEPH', 'JuiceFS', 'Lustre+MinIO']
dfs = {storage: df[df['Storage'] == storage] for storage in storages}

# Prepare data for meshgrid
def prepare_data(df):
    sizes, workers = np.unique(df['Size_KB']), np.unique(df['Wkrs'])
    sizes_grid, workers_grid = np.meshgrid(sizes, workers)
    res_time_grid = np.array([
        [df[(df['Size_KB'] == size) & (df['Wkrs'] == worker)]['Avg-ResTime'].values[0] 
         for size in sizes] for worker in workers
    ])
    return sizes, workers, sizes_grid, workers_grid, res_time_grid

data = {storage: prepare_data(dfs[storage]) for storage in storages}

# Fit linear regression and predict
def fit_and_predict(sizes_grid, workers_grid, res_time_grid):
    reg = LinearRegression().fit(
        np.vstack([sizes_grid.ravel(), workers_grid.ravel()]).T, res_time_grid.ravel()
    )
    return reg.predict(np.vstack([sizes_grid.ravel(), workers_grid.ravel()]).T).reshape(sizes_grid.shape)

preds = {storage: fit_and_predict(*data[storage][2:]) for storage in storages}

# Plot 3D surface
def plot_3d_surface(ax, sizes_grid, workers_grid, res_time_grid, pred, sizes, title):
    ax.plot_surface(sizes_grid, workers_grid, res_time_grid, color='#ff7f0e', alpha=1.0)
    ax.plot_surface(sizes_grid, workers_grid, pred, color='#1f77b4', alpha=0.5)
    ax.set_xlabel('Object sizes (MB)', labelpad=15, fontsize=16)
    ax.set_ylabel('Workers', labelpad=15, fontsize=16)
    ax.set_zlabel('Response Time (ms)', labelpad=20, fontsize=16)
    ax.set_xticks(sizes)
    size_labels = {4: '', 4096: '', 65536: '64', 262144: '256', 1048576: '1024'}
    ax.set_xticklabels([size_labels.get(size, '') for size in sizes], fontsize=14)
    ax.tick_params(axis='both', which='major', labelsize=13)
    ax.view_init(elev=20, azim=75)
    ax.legend(
        [plt.Line2D([0], [0], linestyle='none', marker='o', color=c) 
         for c in ['#ff7f0e', '#1f77b4']], 
        [f'Actual {title}', 'Predicted'], loc='best', prop={'size': 16}
    )

# Plotting
fig = plt.figure(figsize=(17, 7))
for i, storage in enumerate(storages):
    ax = fig.add_subplot(1, 3, i + 1, projection='3d')
    plot_3d_surface(ax, *data[storage][2:], preds[storage], data[storage][0], storage)
    ax.set_yticks([0, 500, 1000])
    ax.set_yticklabels([0, 500, 1000], fontsize=14)

plt.subplots_adjust(wspace=0.3)

# Save plot as EPS file
plt.savefig('output/fig3.eps', format='eps', dpi=300, bbox_inches='tight', pad_inches=0.35)

plt.show()
