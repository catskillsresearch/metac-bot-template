import os, json, requests
import load_secrets
load_secrets.load_secrets()

def jsx_request(jsxRequest):

    """The JSX requests using curl have this format:

        curl -X POST \
          -b "lumAuth={os.getenv('GLIMT_API_KEY')}" \
          -H "Content-Type: application/json;charset=utf-8" \
          -d 'jsxRequest' \
          "https://glimt.nu/glimt-jsx/jsx.json?lang=en"
        
        **Response text:** the text returned by a JSX request is itself always wrapped inside a JSON array. 
        Therefore, below, when we say that a request returns value X, it really means that it returns [ X ] . 
        
        If the response  text does not start by '[', i.e. is not a JSON Array, it indicates an error which is described more or less opaquely in the reply."""

    url = "https://glimt.nu/glimt-jsx/jsx.json?lang=en"
    
    headers = {
        "Content-Type": "application/json;charset=utf-8"
    }
    
    cookies = {
        "lumAuth": os.getenv("GLIMT_API_KEY")
    }
       
    response = requests.post(url, headers=headers, cookies=cookies, data=jsxRequest)
    
    print(response.status_code)

    return json.loads(response.text)