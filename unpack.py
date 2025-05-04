def unpack(q):
    qv = vars(q)
    id = qv['id_of_question']
    question_text = qv['question_text']
    resolution = qv['api_json']['question']['resolution']
    options = repr(qv['api_json']['question']['options'])
    resolution_criteria = qv['resolution_criteria']
    fine_print = qv['fine_print']
    background_info = qv['background_info']
    question_description = qv['api_json']['question']['description']
    title = qv['api_json']['title']
    curation_status = qv['api_json']['curation_status']
    status = qv['api_json']['status']
    vote = qv['api_json']['vote']
    
    fields = [
    id,
    question_text,
    resolution,
    options,
    resolution_criteria,
    fine_print,
    background_info,
    question_description,
    title]

    flds =  [
    "id",
    "question_text",
    "resolution",
        "options",
    "resolution_criteria",
    "fine_print",
    "background_info",
    "question_description",
    "title"]
    return fields, flds