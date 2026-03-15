import pandas as pd
from typing import Optional
from pipeline.utils.file_utils import setup_logger, validate_dataset_path

logger = setup_logger('csv_loader')

class CSVLoader:
    def __init__(self, filepath: str):
        self.filepath = filepath
        self.data: Optional[pd.DataFrame] = None

    def load_data(self) -> pd.DataFrame:
        """
        Load datasets from CSV, validate format, detect column types and missing values.
        """
        logger.info(f"Attempting to load data from {self.filepath}")
        
        if not validate_dataset_path(self.filepath):
            logger.error(f"File not found or invalid: {self.filepath}")
            raise FileNotFoundError(f"Dataset file not found: {self.filepath}")
            
        if not self.filepath.lower().endswith('.csv'):
            logger.error("Invalid format: Dataset must be a CSV file.")
            raise ValueError("Dataset must be a CSV file.")
            
        try:
            self.data = pd.read_csv(self.filepath)
            
            # Log dataset size
            logger.info(f"Dataset loaded successfully. Size: {self.data.shape[0]} rows, {self.data.shape[1]} columns")
            
            # Log column types
            logger.info("Column Types:")
            for col, dtype in self.data.dtypes.items():
                logger.info(f"  - {col}: {dtype}")
                
            # Detect missing values
            missing_values = self.data.isnull().sum()
            total_missing = missing_values.sum()
            if total_missing > 0:
                logger.warning(f"Detected {total_missing} missing values across the dataset.")
                for col, count in missing_values.items():
                    if count > 0:
                        logger.warning(f"  - {col}: {count} missing values")
            else:
                logger.info("No missing values detected.")
                
            return self.data
            
        except Exception as e:
            logger.error(f"Error loading CSV file: {str(e)}")
            raise
