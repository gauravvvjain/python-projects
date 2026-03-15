import sys
import os
import argparse
from pipeline.utils.file_utils import setup_logger, ensure_directory_exists
from pipeline.ingestion.csv_loader import CSVLoader
from pipeline.cleaning.cleaning_engine import CleaningEngine
from pipeline.transformation.transform_engine import TransformEngine
from pipeline.analytics.analysis_engine import AnalysisEngine
from pipeline.graph_analysis.graph_engine import GraphEngine
from pipeline.visualization.visual_engine import VisualEngine
from pipeline.report.report_generator import ReportGenerator

logger = setup_logger('main_pipeline')

def run_pipeline(dataset_path: str):
    logger.info("Initializing Data Processing and Analytics Pipeline.")

    output_base_dir = "data_pipeline_project/data/processed"
    ensure_directory_exists(output_base_dir)

    try:
        # 1. Ingestion
        logger.info("=== STAGE 1: INGESTION ===")
        loader = CSVLoader(filepath=dataset_path)
        raw_data = loader.load_data()
        original_shape = raw_data.shape

        # 2. Cleaning
        logger.info("=== STAGE 2: CLEANING ===")
        cleaner = CleaningEngine(data=raw_data)
        cleaned_data = cleaner.run_cleaning_pipeline()

        # 3. Transformation
        logger.info("=== STAGE 3: TRANSFORMATION ===")
        transformer = TransformEngine(data=cleaned_data)
        # using standard scaler as default
        transformed_data = transformer.run_transformation_pipeline(scale_method='standardize')

        # Save processed dataset
        processed_data_path = os.path.join(output_base_dir, "processed_dataset.csv")
        transformed_data.to_csv(processed_data_path, index=False)
        logger.info(f"Processed dataset saved to {processed_data_path}")

        # 4. Analytics
        logger.info("=== STAGE 4: ANALYTICS ===")
        analyzer = AnalysisEngine(data=transformed_data)
        analytics_results = analyzer.run_analytics_pipeline()

        # 5. Graph Analysis
        logger.info("=== STAGE 5: GRAPH ANALYSIS ===")
        corr_matrix = analytics_results['correlation_matrix']
        graph_engine = GraphEngine(correlation_matrix=corr_matrix, threshold=0.6)
        graph_results = graph_engine.run_graph_pipeline()

        # 6. Visualization
        logger.info("=== STAGE 6: VISUALIZATION ===")
        visual_dir = os.path.join(output_base_dir, "visualizations")
        visualizer = VisualEngine(data=transformed_data, output_dir=visual_dir)
        visualizer.run_visual_pipeline(corr_matrix=corr_matrix)

        # 7. Report Generation
        logger.info("=== STAGE 7: REPORT GENERATION ===")
        report_dir = os.path.join(output_base_dir, "report")
        report_gen = ReportGenerator(output_dir=report_dir)
        report_gen.generate_report(
            original_shape=original_shape,
            final_shape=transformed_data.shape,
            analytics_results=analytics_results,
            graph_results=graph_results,
            visual_path=visual_dir
        )

        logger.info("Pipeline executed successfully! Output available in 'data_pipeline_project/data/processed'")

    except Exception as e:
        logger.error(f"Pipeline failed: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Scalable Data Processing and Analytics Pipeline")
    parser.add_argument("dataset", help="Path to the input CSV dataset")
    args = parser.parse_args()

    # Assuming execution from project directory

    run_pipeline(args.dataset)
