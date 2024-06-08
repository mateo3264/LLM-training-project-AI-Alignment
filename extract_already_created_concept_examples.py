import re


def get_titles_of_examples(file_data, concept):
    try:
        cai = file_data[concept]

        pattern = '\*\*(.*?)\*\*' 

        list_of_titles_of_examples = re.findall(pattern, cai)

        return list_of_titles_of_examples
    except:
        return []