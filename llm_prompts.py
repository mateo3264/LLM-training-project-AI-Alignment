#choose concept

class LLMInputs:
    def __init__(self, main_concept):
        self.main_concept = main_concept
        self.mha_input = 'Based on the analysis of the behavioral analyst T.V. Layng find the defining characteristics/parts/steps (Must Have Attributes) of the concept {main_concept}'
        self.mha_input = self._get_set_mha_input()
        self.manual_multiquery = [
        "How to teach a concept based on T.V. Layng's analysis", 
        'What are the defining characteristics of the concept of {main_concept}',
        'What are the examples T.V. Layng gives to find the defining characteristics',
        'What are the defining and variable characteristics of chairs, belief, bacteria, solid, liquid, gas?',
        'What is a rational set?'
        ]
        self.manual_multiquery = self._get_multiquery()


    
    def _get_set_mha_input(self):
        return self.mha_input.format(main_concept=self.main_concept)
    
    def _get_multiquery(self):
        multiquery_list = []
        for manual_query in self.manual_multiquery:
            multiquery_list.append(manual_query.format(main_concept=self.main_concept))
    
        return multiquery_list
    




MHA_TEMPLATE = '''Based on the following context enumerate and describe each of the defining characteristics of the concept {concept} as detailed by T.V. Layng:

context: {context}
'''

json_examples_format = '''Also use json format for your response and don't put delimiters to indicate it is json, just respond in json 
and because each example is a dict, put all of them in a list in the following way:
"Example 1":[NAME_OF_EXAMPLE],
"[NAME_OF_THE_CHARACTERISTIC_X]":xxxxx,
Defining Characteristics: '''

#Constitutional AI, "Example 2: TITLE, NAME_OF_THE_CHARACTERISTIC_X:xxxx"
csv_examples_format = '''Use a csv format so that the concept goes at the left of the comma and the examples go to the right of the comma as a single string. Don't put any delimiters indicating it is in csv format. like this:
Constitutional AI, "Example 1: **TITLE**, NAME_OF_THE_CHARACTERISTIC_X:xxxx, Example 2: **TITLE**, NAME_OF_THE_CHARACTERISTIC_X:xxxx"
'''

EXAMPLES_TEMPLATE = '''Based on the given defining characteristics of the {concept} concept, give 6 examples as defined by T.V. Layng when he talks about the concept of a rational set.
Make sure that each of the examples have all of the defining characteristics and follow the definition and description of each defining characteristic to generate good examples. Generate different examples than these ones bellow (if there aren't any omit this last part):
Existing Examples:
{existing_examples}
Examples Format:
{examples_format}
Defining Characteristics:
{defining_characteristics}

Answer:
'''

NONEXAMPLES_TEMPLATE = '''Based on the characteristics of the concept of {concept} make 3 nonexamples. Express the removed characteristic. A nonexample is a concept that lacks only one (1) of the defining characteristics. Here is an example:
Concept:
Bacteria
Characteristics:
- Unicellular
- Prokaryote
Answer: Let's choose one characteristic to remove at random. Unicellular. So I have to generate 3
concepts that are multicellular AND prokaryote. There aren't any organisms which are both unicellular and
prokaryote so let's choose another characteristic to remove. Prokaryote. So I have to generate 3
concepts that are unicellular AND eukaryote. 
1- Amoeba (unicellular, eukaryote).
2- Paramecium (unicellular, eukaryote).
3- Euglena (unicellular, eukaryote).


Concept: 
{concept}
Characteristics:
{defining_characteristics}
Answer: 
'''

