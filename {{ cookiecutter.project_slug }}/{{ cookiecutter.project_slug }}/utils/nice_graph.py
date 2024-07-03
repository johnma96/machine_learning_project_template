import numpy as np
import pandas as pd 
import matplotlib.pyplot as plt
import seaborn as sns
from .remove_outliers import RemoveOutliers

class NiceGraph:

    def __init__(self) -> None:
        pass

    def nice_axis(self, ax, color='grey', ticks_labelsize=12, axis_labelsize=13, title_size=14):
        ax.spines['right'].set_visible(False)
        ax.spines['top'].set_visible(False)
        ax.spines['bottom'].set_color(color)
        ax.spines['left'].set_color(color)
        ax.tick_params(axis='x', colors=color, which='both', labelsize=ticks_labelsize)
        ax.tick_params(axis='y', colors=color, which='both', labelsize=ticks_labelsize)
        ax.yaxis.label.set_color(color)
        ax.xaxis.label.set_color(color)
        ax.yaxis.label.set_size(axis_labelsize)
        ax.xaxis.label.set_size(axis_labelsize)
        ax.title.set_color(color)
        ax.title.set_fontsize(title_size)
        
        return ax

    def category_count(self, data, figure_path, save_fig = False, show_plot = False, **kwargs):

        if isinstance(data, pd.Series):
            kwargs['x'] = data.name
            data = data.to_frame()

        if not 'palette' in kwargs.keys():
            kwargs['palette'] = 'twilight'       

        fig = plt.figure(figsize=(8, 6))
        ax = sns.countplot(data=data, **kwargs)

        # Display values over the bars
        for p in ax.patches:
            ax.annotate(f"{p.get_height()}", (p.get_x() + p.get_width() / 2., p.get_height()), ha='center', va='bottom')

        ax = self.nice_axis(ax=ax)
        plt.title(f"Counts of categories in {kwargs['x']}")
        plt.xlabel(kwargs['x'])
        plt.ylabel('Count')

        if not show_plot:
            plt.close()
            
        if save_fig:
            fig.savefig(figure_path, bbox_inches='tight', pad_inches=0.5)

    def histogram(self, data: pd.Series, figure_path: str = 'histogram', 
                show_metrics: bool = False,
                remove_out: bool = False,
                method = 'zscore',
                show_plot: bool = False, save_fig: bool = False, **kwargs):
                
        # Outlier removal
        remove_dict = dict((k, v) for k, v in kwargs.items() if k in ['save_log', 'log_file'])
        zscore_dict = dict((k, v) for k, v in kwargs.items() if k in ['threshold_zscore'])
        lof_dict = dict((k, v) for k, v in kwargs.items() if k in ['n_neighbors', 'contamination'])

        if remove_out:
            remove = RemoveOutliers(**{**remove_dict, 'inplace': True})

            if method == 'zscore':
                if len(zscore_dict) == 0:
                    pos_normal, pos_outliers, data = remove.zscore(data=data)
                else:
                    pos_normal, pos_outliers, data = remove.zscore(data=data, **zscore_dict)

            elif method == 'interquartile':
                    pos_normal, pos_outliers, data = remove.interquartile(data=data)

            elif method == 'lof':
                    if len(lof_dict.keys()) == 0:
                        pos_normal, pos_outliers, data = remove.lof(data=data)
                    else:
                        pos_normal, pos_outliers, data = remove.lof(data=data, **lof_dict)
            else:
                raise ValueError(f"{method} method isn't available")
            
        kwargs = {k: v for k, v in kwargs.items() if (k not in remove_dict.keys()) and (k not in zscore_dict.keys()) and (k not in lof_dict.keys())}
        
        # Plot histogram
        if not ('color' in kwargs.keys()):
            kwargs['color'] = 'grey' 

        if 'ax' in kwargs.keys(): 
            ax = kwargs['ax']
            kwargs.pop('ax')
        else:
            fig, ax = plt.subplots(1,1)

        n, bins, patches = ax.hist(data, edgecolor='black', **kwargs)
        
        plt.xlabel(f"{data.name}".upper())
        y_label = 'Quantity'
        if 'density' in kwargs:
            y_label = 'Percentage'
        plt.ylabel(y_label)
        plt.title(f"Distribution of {data.name}")

        ax = self.nice_axis(ax=ax)

        if show_metrics: 
            palette = sns.color_palette("Reds_r")
            summary_stats = data.describe()
            metrics = ['mean', '25%', '50%', '75%', 'min', 'max']

            y_pos = (np.max(n) - np.min(n))/2
            x_pos_correction = abs(bins[-1] - bins[-2])*1.5

            for i, metric in enumerate(metrics):
                ax.axvline(summary_stats[metric], color=palette[i], linestyle='--', linewidth=2)
                if metric in ['25%', '75%', 'min', 'max', 'mean']:
                    ax.text(summary_stats[metric]-x_pos_correction, y_pos, f'{metric}: {summary_stats[metric]:.3f}', color=palette[i], rotation='vertical')
                else:
                    ax.text(summary_stats[metric]-x_pos_correction, np.max(n) - 0.3*np.std(n), f'{metric}: {summary_stats[metric]:.3f}', color=palette[i], rotation='vertical')
        
        if not show_plot:
            plt.close()

        if save_fig:
            fig.savefig(figure_path, bbox_inches='tight', pad_inches=0.5)

        return ax

    def histograms(self, data: pd.DataFrame,
                        nrows,
                        ncols, 
                        figure_path = 'histograms',
                        show_metrics = False,
                        density = True,
                        save_fig=False,
                        figsize=(12,20),
                        **kwargs):
        
        fig, ax = plt.subplots(nrows=nrows, ncols=ncols, figsize=figsize)
        ax = ax.flat

        for i, col in enumerate(data.columns):
            ax_ = self.histogram(data.loc[:,col],  bins=30, ax = ax[i], density=density, show_metrics=show_metrics, **kwargs)
            ax_.set_title('')
            ax_.set_ylabel('')
            if i%ncols == 0:
                if density: y_label = 'Percentage'
                else: y_label = 'Amount'
                ax_.set_ylabel(y_label)
            ax_ = self.nice_axis(ax=ax_)
            ax_.set_xlabel(str(col).upper())

        fig.suptitle('Distributions', y = 1.01, color = 'grey', fontsize=14)
        fig.tight_layout()

        if save_fig:
            fig.savefig(figure_path, bbox_inches='tight', pad_inches=0.5)
        
        return fig, ax

    def boxplot(self, data: pd.Series, show_plot = True, save_fig = False, figure_path: str = 'boxplot', show_metrics: bool = False, **kwargs):

        if not ('color' in kwargs.keys()):
            kwargs['color'] = 'grey' 

        if 'ax' in kwargs.keys(): 
            ax = kwargs['ax']
            kwargs.pop('ax')
        else:
            fig, ax = plt.subplots(1,1, figsize=(8, 5))

        ax = sns.boxplot(x=data, ax=ax, color=kwargs['color'])
        
        if show_metrics: 
            summary_stats = data.describe()
            metrics_str = '\n'.join([f'{metric}: {value:.3f}' for metric, value in summary_stats.items()])
            ax.text(summary_stats['min'] + summary_stats['std'], 0.4, metrics_str, color='k')

        plt.title(f"Boxplot of {data.name}")

        ax = self.nice_axis(ax=ax)
        
        if not show_plot:
            plt.close()

        if save_fig:
            fig.savefig(figure_path, bbox_inches='tight', pad_inches=0.5)

        return ax

    def boxplots(self, data: pd.DataFrame,
                    nrows,
                    ncols, 
                    figure_path = 'boxplots',
                    show_metrics = False,
                    save_fig = False,
                    figsize = (12,18),
                    **kwargs):
    
        fig, ax = plt.subplots(nrows=nrows, ncols=ncols, figsize=figsize)
        ax = ax.flat

        for i, col in enumerate(data.columns):
            ax_ = self.boxplot(data.loc[:,col], ax = ax[i], show_metrics=show_metrics, **kwargs)
            ax_.set_title('')
            ax_.set_ylabel('')
            ax_ = self.nice_axis(ax=ax_)
            ax_.set_xlabel(str(col).upper())

        fig.suptitle('Boxplots', y = 1.01, color = 'grey', fontsize=14)
        fig.tight_layout()

        if save_fig:
            fig.savefig(figure_path, bbox_inches='tight', pad_inches=0.5)
        
        return fig, ax