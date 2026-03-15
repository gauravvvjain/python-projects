import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from pipeline.utils.file_utils import setup_logger, ensure_directory_exists

logger = setup_logger('visual_engine')

class VisualEngine:
    def __init__(self, data: pd.DataFrame, output_dir: str = "data_pipeline_project/data/processed/visualizations"):
        self.data = data
        self.output_dir = output_dir
        ensure_directory_exists(self.output_dir)

    def generate_histograms(self) -> None:
        """Generate and save histograms for numerical columns."""
        numeric_cols = self.data.select_dtypes(include=[np.number]).columns
        if not numeric_cols.empty:
            for col in numeric_cols:
                plt.figure(figsize=(8, 6))
                sns.histplot(self.data[col], kde=True)
                plt.title(f'Histogram of {col}')
                plt.xlabel(col)
                plt.ylabel('Frequency')
                
                filepath = os.path.join(self.output_dir, f'histogram_{col}.png')
                plt.savefig(filepath)
                plt.close()
            logger.info(f"Generated histograms in {self.output_dir}")

    def generate_scatter_plots(self, max_pairs: int = 5) -> None:
        """Generate and save scatter plots for pairs of numerical columns."""
        numeric_cols = self.data.select_dtypes(include=[np.number]).columns
        if len(numeric_cols) >= 2:
            pairs_plotted = 0
            for i in range(len(numeric_cols)):
                for j in range(i + 1, len(numeric_cols)):
                    col1 = numeric_cols[i]
                    col2 = numeric_cols[j]
                    
                    plt.figure(figsize=(8, 6))
                    sns.scatterplot(data=self.data, x=col1, y=col2)
                    plt.title(f'Scatter Plot: {col1} vs {col2}')
                    
                    filepath = os.path.join(self.output_dir, f'scatter_{col1}_vs_{col2}.png')
                    plt.savefig(filepath)
                    plt.close()
                    
                    pairs_plotted += 1
                    if pairs_plotted >= max_pairs:
                        break
                if pairs_plotted >= max_pairs:
                    break
            logger.info(f"Generated {pairs_plotted} scatter plots in {self.output_dir}")

    def generate_correlation_heatmap(self, corr_matrix: pd.DataFrame) -> None:
        """Generate and save correlation heatmap."""
        if not corr_matrix.empty:
            plt.figure(figsize=(10, 8))
            sns.heatmap(corr_matrix, annot=True, cmap='coolwarm', fmt='.2f')
            plt.title('Feature Correlation Heatmap')
            
            filepath = os.path.join(self.output_dir, 'correlation_heatmap.png')
            plt.savefig(filepath)
            plt.close()
            logger.info(f"Generated correlation heatmap at {filepath}")

    def generate_feature_distribution_plots(self) -> None:
        """Generate feature distribution plots (box plots) for numerical columns."""
        numeric_cols = self.data.select_dtypes(include=[np.number]).columns
        if not numeric_cols.empty:
            for col in numeric_cols:
                plt.figure(figsize=(8, 6))
                sns.boxplot(y=self.data[col])
                plt.title(f'Distribution of {col}')
                
                filepath = os.path.join(self.output_dir, f'distribution_{col}.png')
                plt.savefig(filepath)
                plt.close()
            logger.info(f"Generated feature distribution plots in {self.output_dir}")

    def run_visual_pipeline(self, corr_matrix: pd.DataFrame) -> None:
        """Execute all visualization tasks."""
        logger.info("Starting visualization pipeline...")
        self.generate_histograms()
        self.generate_scatter_plots()
        self.generate_correlation_heatmap(corr_matrix)
        self.generate_feature_distribution_plots()
        logger.info("Visualization pipeline completed successfully.")
