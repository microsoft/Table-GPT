from .base_table_task import BaseTableTask
from .column_augmentation import ColumnAugmentation
from .column_finding import ColumnFinding
from .column_type_annotation import ColumnTypeAnnotation
from .data_imputation import DataImputation
from .entity_matching import EntityMatching
from .error_detection import ErrorDetection
from .header_value_matching import HeaderValueMatching
from .missing_value_identification import MissingValueIdentification
from .row_augmentation import RowAugmentation
from .nl2sql import NL2SQL
from .table_question import TableQuestion
from .schema_matching import SchemaMatching
from .row_to_row_transformation import Row2RowTransformation
from .row_column_filtering import RowColumnFiltering
from .row_column_sorting import RowColumnSorting
from .row_column_swapping import RowColumnSwapping
from .list_extraction import ListExtraction
from .table_summary import TableSummary


class TableTaskFactory:
    @classmethod
    def get_table_task(self, task_name: str) -> BaseTableTask:
        if task_name == "DataImputation":
            return DataImputation()
        elif task_name == "ColumnAugmentation":
            return ColumnAugmentation()
        elif task_name == "ColumnFinding":
            return ColumnFinding()
        elif task_name == "ColumnTypeAnnotation":
            return ColumnTypeAnnotation()
        elif task_name == "EntityMatching":
            return EntityMatching()
        elif task_name == "ErrorDetection":
            return ErrorDetection()
        elif task_name == "HeaderValueMatching":
            return HeaderValueMatching()
        elif task_name == "MissingValueIdentification":
            return MissingValueIdentification()
        elif task_name == "RowAugmentation":
            return RowAugmentation()
        elif task_name == "NL2SQL":
            return NL2SQL()
        elif task_name == "TableQuestion":
            return TableQuestion()
        elif task_name == "SchemaMatching":
            return SchemaMatching()
        elif task_name == "Row2RowTransformation":
            return Row2RowTransformation()
        elif task_name == "RowColumnFiltering":
            return RowColumnFiltering()
        elif task_name == "RowColumnSorting":
            return RowColumnSorting()
        elif task_name == "RowColumnSwapping":
            return RowColumnSwapping()
        elif task_name == "ListExtraction":
            return ListExtraction()
        elif task_name == "TableSummary":
            return TableSummary()
        else:
            raise Exception(f"Wrong task name {task_name}")
