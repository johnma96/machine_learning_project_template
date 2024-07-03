import numpy as np
import pandas as pd
from scipy.stats import zscore
from sklearn.neighbors import LocalOutlierFactor


class RemoveOutliers:

    def __init__(self, inplace: bool = False, save_log: bool = False, log_file: bool = 'output.txt') -> None:
        self.save_log = save_log
        self.log_file = log_file
        self.inplace = inplace


    def __make_actions(self, data, normals_position, outliers_position):

        data_shape_orig = data.shape
        proportion_remotion = (len(outliers_position))/(data_shape_orig[0])

        if self.save_log:
            with open(self.log_file, 'a') as f:
                print(f"{len(outliers_position)} points removed from a total of {data_shape_orig[0]} using {self.method} method. It represent {proportion_remotion*100:.3f}% for {data.name} variable", file=f)
        else:
            print(f"{len(outliers_position)} points removed from a total of {data_shape_orig[0]} using {self.method} method. It represent {proportion_remotion*100:.3f}% for {data.name} variable")

        if self.inplace:
            return normals_position, outliers_position, data[normals_position]
        else:
            return normals_position, outliers_position, data

    def zscore(self, data, threshold_zscore: int = 3):
        self.method = 'zscore'

        zscores = zscore(data)
        outliers_position = np.where(np.abs(zscores) > threshold_zscore)[0]
        normals_position = np.where(np.abs(zscores) <= threshold_zscore)[0]

        return self.__make_actions(data, normals_position, outliers_position)
    
    def interquartile(self, data):
        self.method = 'interquartile'

        # Calculate IQR
        q1 = np.percentile(data, 25)
        q3 = np.percentile(data, 75)
        iqr = q3 - q1

        # Define outlier boundaries using IQR method
        lower_bound = q1 - 1.5 * iqr
        upper_bound = q3 + 1.5 * iqr

        # Detect outliers using IQR method
        outliers_position = np.where((data < lower_bound) | (data > upper_bound))[0]
        normals_position = np.where((data >= lower_bound) & (data <= upper_bound))[0]

        return self.__make_actions(data, normals_position, outliers_position)
    
    def lof(self, data, n_neighbors: int = 20, contamination: float = 0.01):
        self.method = 'lof'

        outlier_factor = LocalOutlierFactor(n_neighbors=n_neighbors, contamination=contamination)
        outliers = outlier_factor.fit_predict(data.values.reshape(-1, 1))

        outliers_position = np.where(outliers == -1)[0]
        normals_position = np.where(outliers == 1)[0]

        return self.__make_actions(data, normals_position, outliers_position)



def remove_outliers_(data: pd.Series, 
                    method: str = 'zscore',
                    threshold_zscore: int = 3,
                    n_neighbors_lof: int = 20,
                    contamination_lof: float = 0.01,
                    inplace: bool = False,
                    save_log: bool = False,
                    log_file: bool = 'output.txt'
    ):

    if method == 'zscore': 
        
        zscores = zscore(data)
        pos_outliers = np.where(np.abs(zscores) > threshold_zscore)[0]
        pos_normal = np.where(np.abs(zscores) <= threshold_zscore)[0]
        
    elif method == 'interquartile':
        # Calculate IQR
        q1 = np.percentile(data, 25)
        q3 = np.percentile(data, 75)
        iqr = q3 - q1

        # Define outlier boundaries using IQR method
        lower_bound = q1 - 1.5 * iqr
        upper_bound = q3 + 1.5 * iqr

        # Detect outliers using IQR method
        pos_outliers = np.where((data < lower_bound) | (data > upper_bound))[0]
        pos_normal = np.where((data >= lower_bound) & (data <= upper_bound))[0]


    elif method.upper() == 'LOF':
        outlier_factor = LocalOutlierFactor(n_neighbors=n_neighbors_lof, contamination=contamination_lof)
        outliers = outlier_factor.fit_predict(data.values.reshape(-1, 1))

        pos_outliers = np.where(outliers == -1)[0]
        pos_normal = np.where(outliers == 1)[0]

    else:
        raise ValueError(f"{method} method isn't available")
    
    data_shape_orig = data.shape
    proportion_remotion = (len(pos_outliers))/(data_shape_orig[0])

    if save_log:
        with open(log_file, 'a') as f:
            print(f"{len(pos_outliers)} points removed from a total of {data_shape_orig[0]} using {method} method. It represent {proportion_remotion*100:.3f}% for {data.name} variable", file=f)
    else:
        print(f"{len(pos_outliers)} points removed from a total of {data_shape_orig[0]} using {method} method. It represent {proportion_remotion*100:.3f}% for {data.name} variable")
        
    
    if inplace:
        data = data[pos_normal]
        return pos_normal, pos_outliers, data

    else:
        return pos_normal, pos_outliers