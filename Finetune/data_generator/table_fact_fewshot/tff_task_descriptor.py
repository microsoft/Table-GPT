from ..base.base_task_descriptor import BaseTaskDescriptor

class TFFTaskDescriptor(BaseTaskDescriptor):
    def _get_task_description(self, random_state=None):
        descriptions = [
            "Please look at the table, and then determine the statement is True or False."
        ]
        return self.select_one_option(descriptions, random_state=random_state)

    def get_input(self, data, random_state=None):
        cot = """
*Table Caption:* 1919 in brazilian football
*Table:*
|Unnamed: 0|date|result|score|brazil scorers|competition|
|---|---|---|---|---|---|
|0|may 11 , 1919|w|6 - 0|friedenreich (3) , neco (2) , haroldo|south american championship|
|1|may 18 , 1919|w|3 - 1|heitor , amílcar , millon|south american championship|
|2|may 26 , 1919|d|2 - 2|neco (2)|south american championship|
|3|may 29 , 1919|w|1 - 0|friedenreich|south american championship|
|4|june 1 , 1919|d|3 - 3|haroldo , arlindo (2)|taça roberto cherry|

*Statement:*
haroldo be mention as a brazil scorer for 2 different game

## Output:
In the table above, the "brazil scorers" column mentions "haroldo" in the following rows:
|0|may 11 , 1919|w|6 - 0|friedenreich (3) , neco (2) , haroldo|south american championship|
|4|june 1 , 1919|d|3 - 3|haroldo , arlindo (2)|taça roberto cherry|

There are a total of 2 rows, corresponding to two games, that mention "haroldo" as a "brazil scorer". Therefore, the statement is true. The final answer is {\"answer\": \"True\"}.

## Input:
*Table Caption:* east kent mavericks
*Table:*
|Unnamed: 0|season|division|wins|ties|final position|
|---|---|---|---|---|---|
|0|2001|british senior flag league , southern|3|1|2 / 4|
|1|2002|british senior flag league , nine - man league|5|3|2 / 7|
|2|2003 to 2005|did not compete|did not compete|did not compete|did not compete|
|3|2006|bafl division two south|0|0|4 / 4|
|4|2007|bafl division two south east|5|0|3 / 6|
|5|2008|bafl division two south east|6|0|3 / 5|
|6|2009|bafl division two south east|8|1|1 / 4|
|7|2010|bafl division one south east|8|1|1 / 4|
|8|2011|bafl division one south east|2|6||
|9|2012|bafl division one south and central|8|2|8 / 2|

*Statement:*
the lowest number of win be during the 2009 , 2012 , and 2010 season

## Output:
In the table above, the "season" and "wins" columns show that, in year 2006 there are 0 win, in year 2011 there are 2 wins, in year 2001 there are 3 wins, which are the lowest in the table. So from the table, the lowest number of win should be during the 2006 , 2011 , and 2001 season. Therefore, the statement is false. The final answer is {\"answer\": \"False\"}.

## Input:
*Table Caption:* 5th united states congress
*Table:*
|Unnamed: 0|district|vacator|reason for change|successor|date successor seated|
|---|---|---|---|---|---|
|0|rhode island at - large|elisha potter ( f )|resigned sometime in 1797|thomas tillinghast ( f )|seated november 13 , 1797|
|1|south carolina 1st|william l smith ( f )|resigned july 10 , 1797|thomas pinckney ( f )|seated november 23 , 1797|
|2|massachusetts 11th|theophilus bradbury ( f )|resigned july 24 , 1797|bailey bartlett ( f )|seated november 27 , 1797|
|3|new hampshire at - large|jeremiah smith ( f )|resigned july 26 , 1797|peleg sprague ( f )|seated december 15 , 1797|
|4|connecticut at - large|james davenport ( f )|died august 3 , 1797|william edmond ( f )|seated november 13 , 1797|
|5|pennsylvania 5th|george ege ( f )|resigned sometime in october , 1797|joseph hiester ( dr )|seated december 1 , 1797|
|6|pennsylvania 4th|samuel sitgreaves ( f )|resigned sometime in 1798|robert brown ( dr )|seated december 4 , 1798|
|7|north carolina 10th|nathan bryan ( dr )|died june 4 , 1798|richard dobbs spaight ( dr )|seated december 10 , 1798|
|8|pennsylvania 1st|john swanwick ( dr )|died august 1 , 1798|robert waln ( f )|seated december 3 , 1798|
|9|connecticut at - large|joshua coit ( f )|died september 5 , 1798|jonathan brace ( f )|seated december 3 , 1798|

*Statement:*
40% of the 5th congress die in office

## Output:
In the table above titled "5th united states congress", the "reason for change" column shows that the following congressmen died in office:
|4|connecticut at - large|james davenport ( f )|died august 3 , 1797|william edmond ( f )|seated november 13 , 1797|
|7|north carolina 10th|nathan bryan ( dr )|died june 4 , 1798|richard dobbs spaight ( dr )|seated december 10 , 1798|
|8|pennsylvania 1st|john swanwick ( dr )|died august 1 , 1798|robert waln ( f )|seated december 3 , 1798|
|9|connecticut at - large|joshua coit ( f )|died september 5 , 1798|jonathan brace ( f )|seated december 3 , 1798|

Out of the 10 rows representing 10 congressmen in the table, 4 died in office, which is 4/10=40%. This matches the statement "40% of the 5th congress die in office". Therefore, the statement is true. The final answer is {\"answer\": \"True\"}.
"""     
        df, statement, caption = data
        text = (
            f"{cot}\n"
            "## Input:\n"
            f"*Table Caption:* {caption}\n"
            "*Table:*\n"
            f"{self.serializer.serialize_df(df)}\n"
            "*Statement:*\n"
            f"{statement}"
        )
        return text
    
    def _get_output(self, y):
        if y == 0:
            return "False"
        else:
            return "True"
        return y
    
    def get_output_example(self):
        return "answer", "<True or False>"
    