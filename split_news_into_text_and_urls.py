def split_news_into_text_and_urls(ifp, news):
    ### Split news into text and URLs
    ifp_id = ifp['id']
    ifp_news = news[ifp_id]
    s1 = ifp_news.split('\n\n')
    s2 = [x for x in s1 if '\nSource' in x]
    s3 = [x.split('\nSource:') for x in s2]
    ifp_news_text = [x[0].split('\nOriginal language:')[0] for x in s3]
    ifp_news_sources = [x.split('](')[1][0:-1] for x in [x[1] for x in s3]]
    ifp_news = dict([(x,y) for x,y in zip(ifp_news_sources, ifp_news_text)])
    ifp_news_sources = [x for x,y in ifp_news.items()]
    ifp_news_text = [y for x,y in ifp_news.items()]
    return ifp_news_sources, ifp_news_text