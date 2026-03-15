import pandas as pd
import numpy as np
from pipeline.utils.file_utils import setup_logger

logger = setup_logger('cleaning_engine')

class CleaningEngine:
    def __init__(self, data: pd.DataFrame):
        self.data = data.copy()

    def remove_duplicates(self) -> None:
        """Remove duplicate rows from the dataset."""
        initial_shape = self.data.shape[0]
        self.data.drop_duplicates(inplace=True)
        final_shape = self.data.shape[0]
        duplicates_removed = initial_shape - final_shape
        if duplicates_removed > 0:
            logger.info(f"Removed {duplicates_removed} duplicate rows.")
        else:
            logger.info("No duplicate rows found.")

    def handle_missing_values(self) -> None:
        """
        Fill missing values:
        - Numeric columns: median
        - Categorical columns: mode
        """
        numeric_cols = self.data.select_dtypes(include=[np.number]).columns
        categorical_cols = self.data.select_dtypes(exclude=[np.number]).columns

        for col in numeric_cols:
            if self.data[col].isnull().any():
                median_val = self.data[col].median()
                self.data[col] = self.data[col].fillna(median_val)
                logger.info(f"Filled missing values in numeric column '{col}' with median: {median_val}")

        for col in categorical_cols:
            if self.data[col].isnull().any():
                mode_val = self.data[col].mode()[0]
                self.data[col] = self.data[col].fillna(mode_val)
                logger.info(f"Filled missing values in categorical column '{col}' with mode: '{mode_val}'")

    def detect_and_handle_outliers(self, multiplier: float = 1.5) -> None:
        """
        Detect outliers using the IQR method and handle them.
        For simplicity, we cap the values at the lower and upper bounds.
        """
        numeric_cols = self.data.select_dtypes(include=[np.number]).columns

        for col in numeric_cols:
            Q1 = self.data[col].quantile(0.25)
            Q3 = self.data[col].quantile(0.75)
            IQR = Q3 - Q1
            lower_bound = Q1 - multiplier * IQR
            upper_bound = Q3 + multiplier * IQR

            outliers = self.data[(self.data[col] < lower_bound) | (self.data[col] > upper_bound)]
            if not outliers.empty:
                logger.info(f"Detected {len(outliers)} outliers in column '{col}'. Capping to [{lower_bound}, {upper_bound}].")
                # Cap outliers
                self.data[col] = np.where(self.data[col] < lower_bound, lower_bound, self.data[col])
                self.data[col] = np.where(self.data[col] > upper_bound, upper_bound, self.data[col])

    def correct_data_types(self) -> None:
        """
        Attempt to correct data types implicitly. E.g. strings that look like numbers to float.
        """
        # Sometimes numeric values are loaded as 'object' due to some dirty rows.
        # But this requires careful handling.
        categorical_cols = self.data.select_dtypes(include=['object']).columns

        for col in categorical_cols:
            try:
                converted = pd.to_numeric(self.data[col], errors='raise')
                self.data[col] = converted
                logger.info(f"Corrected data type for column '{col}' from object to numeric.")
            except ValueError:
                # If it raises ValueError, it means it's truly categorical (or has non-numeric text)
                pass

    def run_cleaning_pipeline(self) -> pd.DataFrame:
        """Run all cleaning steps in sequence."""
        logger.info("Starting data cleaning pipeline...")
        self.remove_duplicates()
        self.handle_missing_values()
        self.detect_and_handle_outliers()
        self.correct_data_types()
        logger.info("Data cleaning completed successfully.")
        return self.data
