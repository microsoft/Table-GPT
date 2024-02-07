import pandas as pd

class TextSerializer(object):
    def __init__(self, sep_token=".", nan_token=""):
        self.sep_token = sep_token + " "
        self.nan_token = nan_token
        
    def serialize_row(self, row):
        """Turn structured row into string."""
        res = []
        for name, value in row.items():
            if pd.isna(value):
                text = f"{name}: {self.nan_token}"
            else:
                text = f"{name}: {str(value).strip()}"        
            res.append(text.lstrip())        
        return self.sep_token.join(res)

class MarkdownSerializer(object):
    def __init__(self):
        pass
    
    def serialize_row(self, row):
        df = row.to_frame().T
        return self.serialize_df(df)
    
    def serialize_df(self, df):
        return str(df.to_markdown(index=False)).strip()

class MarkdownShortLineSerializer(MarkdownSerializer):
    def serialize_df(self, df):
        text = [""]
        for c in df.columns:
            text.append(str(c))
        text.append("\n")

        # add separating line
        for c in df.columns:
            text.append("---")
        text.append("\n")
        
        for row in df.values:
            for x in row:
                text.append(str(x))
            text.append("\n")
        return "|".join(text)
    
class KeyValueSerializer(MarkdownSerializer):
    def serialize_df(self, df):
        text = [""]
        for i, row in df.iterrows():
            for c, x in row.items():
                text.append(f"{c}: {x}")
            text.append("\n")
        return "|".join(text)

class MarkdownShortSerializer(MarkdownSerializer):
    def serialize_df(self, df):
        text = [""]
        for c in df.columns:
            text.append(str(c))
        text.append("\n")
        
        for row in df.values:
            for x in row:
                text.append(str(x))
            text.append("\n")
        return "|".join(text)
    
class HTMLSerializer(MarkdownSerializer):    
    def serialize_df(self, df):
        return df.to_html()

class JsonSerializer(MarkdownSerializer):    
    def serialize_df(self, df):
        ## dedup column headers
        new_columns = []
        count = {}
        for c in df.columns:
            count[c] = count.get(c, 0) + 1
            if count[c] == 1:
                new_columns.append(c)
            else:
                new_columns.append(c + f'_{count[c]}')
        df.columns = new_columns
        return df.to_json(orient='records', lines=True)
    
class CSVSerializer(MarkdownSerializer):    
    def serialize_df(self, df):
        return df.to_csv(index=False)


### test cases
# df = pd.DataFrame({"a":[1,2,3,4,5], "b": ["xxx", "yyy", "zzz", "aaa", "bbb"], "c": ["eeee", "asad", "asas", "ssss", "sscc"]})
# print(df)
# serializer = MarkdownSerializer()
# serializer = MarkdownShortSerializer()
# serializer = MarkdownShortLineSerializer()
# serializer = KeyValueSerializer()
# serializer = HTMLSerializer()
# serializer = JsonSerializer()

# text = serializer.serialize_df(df)
# print(text + "hello")
# text = serializer.serialize_row(df.iloc[0])
# print(text + "hello")
# text = serializer.serialize_row(df.iloc[1])
# print(text)