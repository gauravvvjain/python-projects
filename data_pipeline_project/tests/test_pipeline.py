import unittest
import pandas as pd
import numpy as np
from pipeline.ingestion.csv_loader import CSVLoader
from pipeline.cleaning.cleaning_engine import CleaningEngine
from pipeline.transformation.transform_engine import TransformEngine
from pipeline.analytics.analysis_engine import AnalysisEngine
from pipeline.graph_analysis.graph_engine import GraphEngine

class TestPipeline(unittest.TestCase):
    def setUp(self):
        # Create a mock dataframe
        self.mock_data = pd.DataFrame({
            'A': [1, 2, np.nan, 4, 100], # 100 is an outlier, np.nan is missing
            'B': ['cat', 'dog', 'cat', np.nan, 'dog'], # missing categorical
            'C': [10.5, 20.1, 15.2, 10.5, 12.3]
        })
        # Add a duplicate row manually for testing duplicate removal
        self.mock_data.loc[5] = self.mock_data.loc[0]

    def test_cleaning_engine(self):
        cleaner = CleaningEngine(self.mock_data)
        cleaned_data = cleaner.run_cleaning_pipeline()
        
        # Check duplicates removed
        self.assertEqual(len(cleaned_data), 5)
        
        # Check missing values handled
        self.assertFalse(cleaned_data.isnull().values.any())
        
        # Check outlier capping (IQR on column A: Q1=1.5, Q3=4.0, IQR=2.5. Upper=4 + 1.5*2.5 = 7.75)
        # So 100 should be capped
        self.assertTrue(cleaned_data['A'].max() < 100)

    def test_transformation_engine(self):
        cleaner = CleaningEngine(self.mock_data)
        cleaned_data = cleaner.run_cleaning_pipeline()
        
        transformer = TransformEngine(cleaned_data)
        transformed_data = transformer.run_transformation_pipeline(scale_method='normalize')
        
        # Check normalization (values between 0 and 1)
        self.assertTrue((transformed_data['A'] >= 0).all() and (transformed_data['A'] <= 1).all())
        
        # Check categorical encoding
        self.assertTrue(pd.api.types.is_numeric_dtype(transformed_data['B']))

    def test_analytics_engine(self):
        cleaner = CleaningEngine(self.mock_data)
        cleaned_data = cleaner.run_cleaning_pipeline()
        transformer = TransformEngine(cleaned_data)
        transformed_data = transformer.run_transformation_pipeline()
        
        analyzer = AnalysisEngine(transformed_data)
        results = analyzer.run_analytics_pipeline()
        
        self.assertIn('descriptive_statistics', results)
        self.assertIn('correlation_matrix', results)
        self.assertEqual(results['correlation_matrix'].shape[0], transformed_data.shape[1])

if __name__ == '__main__':
    unittest.main()
