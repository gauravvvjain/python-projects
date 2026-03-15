import pandas as pd
import numpy as np
from pipeline.utils.file_utils import setup_logger

logger = setup_logger('analysis_engine')

class AnalysisEngine:
    def __init__(self, data: pd.DataFrame):
        self.data = data.copy()

    def compute_descriptive_statistics(self) -> pd.DataFrame:
        """
        Compute mean, median, variance, standard deviation.
        Returns a DataFrame containing these statistics.
        """
        numeric_cols = self.data.select_dtypes(include=[np.number])
        if numeric_cols.empty:
            logger.warning("No numeric columns found to compute statistics.")
            return pd.DataFrame()
        
        stats = {
            'mean': numeric_cols.mean(),
            'median': numeric_cols.median(),
            'variance': numeric_cols.var(),
            'std_dev': numeric_cols.std()
        }
        
        df_stats = pd.DataFrame(stats)
        logger.info("Computed descriptive statistics (mean, median, variance, std_dev).")
        return df_stats

    def compute_column_distributions(self) -> pd.DataFrame:
        """
        Compute general distributions for columns (using info/describe).
        """
        distributions = self.data.describe(include='all')
        logger.info("Computed column distributions.")
        return distributions

    def compute_correlation_matrix(self) -> pd.DataFrame:
        """
        Compute correlation matrix for numerical columns.
        """
        numeric_cols = self.data.select_dtypes(include=[np.number])
        if numeric_cols.empty:
            logger.warning("No numeric columns found for correlation matrix.")
            return pd.DataFrame()
            
        corr_matrix = numeric_cols.corr()
        logger.info("Computed correlation matrix.")
        return corr_matrix

    def compute_feature_importance(self) -> pd.Series:
        """
        Calculate a basic feature importance heuristic based on variance.
        (Features with higher variance might be considered more important in unsupervised settings).
        """
        numeric_cols = self.data.select_dtypes(include=[np.number])
        if numeric_cols.empty:
            logger.warning("No numeric columns found for feature importance.")
            return pd.Series(dtype=float)
            
        variances = numeric_cols.var().sort_values(ascending=False)
        logger.info("Computed feature importance based on variance.")
        return variances

    def run_analytics_pipeline(self) -> dict:
        """
        Run all analytics steps and return a dictionary of results.
        """
        logger.info("Starting data analytics pipeline...")
        results = {
            'descriptive_statistics': self.compute_descriptive_statistics(),
            'column_distributions': self.compute_column_distributions(),
            'correlation_matrix': self.compute_correlation_matrix(),
            'feature_importance': self.compute_feature_importance()
        }
        logger.info("Data analytics pipeline completed.")
        return results
