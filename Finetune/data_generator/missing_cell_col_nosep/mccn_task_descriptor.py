from data_generator.missing_cell_col_sep.mccs_task_descriptor import MCCSTaskDescriptor

class MCCNTaskDescriptor(MCCSTaskDescriptor):
    def get_input(self, df, random_state=None):
        input_text = self.serializer.serialize_df(df)
        return input_text.replace("[MISSING]|", "")