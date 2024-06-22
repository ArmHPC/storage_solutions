import pandas as pd

# Convert sizes from string to numeric value for correct plotting
def convert_size_to_kb(size_str):
    size_map = {
        '4 KB': 4,
        '4 MB': 4 * 1024,
        '64 MB': 64 * 1024,
        '256 MB': 256 * 1024,
        '1024 MB': 1024 * 1024
    }
    return size_map.get(size_str, 0)

# Convert Avg-ResTime column to float type
def convert_avg_restime_to_float(df):
    df['Avg-ResTime'] = df['Avg-ResTime'].str.replace(' ms', '').astype(float)

# Convert Throughput column to float type
def convert_throughput_to_float(df):
    df['Throughput'] = df['Throughput'].str.replace(' op/s', '').astype(float)

# Load and preprocess data from CSV file
def load_and_prepare_data(file_path, is_cosbench=True):
    df = pd.read_csv(file_path)
    if is_cosbench:
        df['Size_KB'] = df['Sizes'].map(convert_size_to_kb)
        convert_avg_restime_to_float(df)
        convert_throughput_to_float(df)
    return df
