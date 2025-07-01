from prompt2_binary import prompt2_binary
from prompt2_multiple_choice import prompt2_multiple_choice
from prompt2_numeric import prompt2_numeric

def prompt2(row, model):
    prompt2s = {'binary': prompt2_binary,
                'multiple_choice': prompt2_multiple_choice,
                'numeric': prompt2_numeric}
    return prompt2s[row.question_type](row, model)
