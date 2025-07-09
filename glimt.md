# HOW TO GLIMT

## JSX Requests

The JSX requests using curl have this format:

curl -X POST \
  -b "lumAuth={os.getenv('GLIMT_API_KEY')}" \
  -H "Content-Type: application/json;charset=utf-8" \
  -d 'jsxRequest' \
  "https://glimt.nu/glimt-jsx/jsx.json?lang=en"
  
Response text: 

the text returned by a JSX request is itself always wrapped inside a JSON array. Therefore, below, when we say that a request returns value X, it really means that it returns [ X ] . 

If the response  text does not start by '[', i.e. is not a JSON Array, it indicates an error which is described more or less opaquely in the reply.

## Query active IFPs

To request the list of active IFPs, replace jsxRequest by:

[["ifps", "queryIFPs", {query: {state: "active"}, fmt: {}}]]

It will return a JSON array of all active iFPs and their detailed properties, including:
* symbol
* title
* details: Information beyond the title of the IFP, such as what sources may be used to resolve the IFP, and/or some background information that might be useful to forecasters, &c.
* bins: An array of the proposed resolution outcomes

## Submit forecast to IFP

To submit a forecast, replace jsxRequest by:

[["ifps","submitAIFcst",{"ifpRef": "symbol","data": {"probas": binProbas },"reasoning": "Because i know."}]]

where you should replace
symbol with the symbol of the IFP for which you are submitting a forecast binProbas with a JSON array of probabilities adding to 1.0, and such that each one corresponds to the IFP's bin (i.e. outcome) at the same index. For example, an IFP with 4 outcomes could accept [0.2, 0.6, 0, 0.2] where 0.6 is the probability you assign to the second outcome.

It will return a JSON object containing the full description of your submitted forecast, including the forecast ID.
