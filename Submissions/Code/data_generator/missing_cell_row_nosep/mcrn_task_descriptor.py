from data_generator.missing_cell_row_sep.mcrs_task_descriptor import MCRSTaskDescriptor

class MCRNTaskDescriptor(MCRSTaskDescriptor):
    def get_input(self, df, random_state=None):
        input_text = self.serializer.serialize_df(df)
        return input_text.replace("[MISSING]|", "")