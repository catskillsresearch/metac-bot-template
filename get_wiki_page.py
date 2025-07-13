import wikipediaapi

language = 'en'
user_agent = wikipediaapi.USER_AGENT
wiki = wikipediaapi.Wikipedia(user_agent,language)

def get_wiki_page(title):

    """Retrieve Wikipedia article text from article name on demand."""
    
    return wiki.page(title)

if __name__=="__main__":
    print(get_wiki_page("Lars"))
