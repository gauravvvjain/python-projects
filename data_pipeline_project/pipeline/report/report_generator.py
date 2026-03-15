import os
import pandas as pd
from pipeline.utils.file_utils import setup_logger, ensure_directory_exists

logger = setup_logger('report_generator')

class ReportGenerator:
    def __init__(self, output_dir: str = "data_pipeline_project/data/processed/report"):
        self.output_dir = output_dir
        ensure_directory_exists(self.output_dir)
        self.report_path = os.path.join(self.output_dir, "report.txt")

    def generate_report(self, 
                        original_shape: tuple,
                        final_shape: tuple,
                        analytics_results: dict, 
                        graph_results: dict,
                        visual_path: str) -> None:
        """
        Generate a final report summarizing:
        dataset statistics, detected anomalies, important correlations, and visualizations.
        """
        logger.info("Generating pipeline final report...")
        
        with open(self.report_path, "w") as f:
            f.write("=" * 50 + "\n")
            f.write("DATA PIPELINE AND ANALYTICS REPORT\n")
            f.write("=" * 50 + "\n\n")

            f.write("1. DATASET OVERVIEW\n")
            f.write("-" * 20 + "\n")
            f.write(f"Original Dataset Shape: {original_shape[0]} rows, {original_shape[1]} columns\n")
            f.write(f"Final Processed Dataset Shape: {final_shape[0]} rows, {final_shape[1]} columns\n\n")

            f.write("2. DESCRIPTIVE STATISTICS\n")
            f.write("-" * 20 + "\n")
            stats_df = analytics_results.get('descriptive_statistics', pd.DataFrame())
            if not stats_df.empty:
                f.write(stats_df.to_string())
            else:
                f.write("No numeric columns available for statistics.")
            f.write("\n\n")

            f.write("3. FEATURE IMPORTANCE (VARIANCE-BASED)\n")
            f.write("-" * 20 + "\n")
            feat_imp = analytics_results.get('feature_importance', pd.Series())
            if not feat_imp.empty:
                f.write(feat_imp.to_string())
            else:
                f.write("N/A")
            f.write("\n\n")

            f.write("4. CORRELATION GRAPH ANALYSIS\n")
            f.write("-" * 20 + "\n")
            if graph_results:
                f.write(f"Number of Highly Correlated Features (Nodes): {graph_results.get('num_nodes', 0)}\n")
                f.write(f"Number of Strong Correlations (Edges): {graph_results.get('num_edges', 0)}\n")
                
                traversals = graph_results.get('traversals', {})
                if 'bfs' in traversals:
                    f.write(f"Sample BFS Traversal from high-correlation sub-graph: {traversals['bfs']}\n")
            else:
                f.write("No strong correlations found above the threshold.\n")
            f.write("\n")

            f.write("5. VISUALIZATIONS GENERATED\n")
            f.write("-" * 20 + "\n")
            f.write(f"Visualizations have been saved successfully to: {visual_path}\n")
            f.write("Check the directory for histograms, scatter plots, feature distributions, and the correlation heatmap.\n")
            f.write("\n")
            
            f.write("=" * 50 + "\n")
            f.write("END OF REPORT\n")
            f.write("=" * 50 + "\n")

        logger.info(f"Report successfully saved to {self.report_path}")
