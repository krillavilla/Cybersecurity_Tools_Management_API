import http.client

conn = http.client.HTTPSConnection("udacity-cofshp.us.auth0.com")

payload = "{\"client_id\":\"dYfY9fLTPlgVE3kgXuHQFGKLp7MfxgyH\",\"client_secret\":\"cXSSMezGQLhVICN5QADumgL4UM5r-B4kqB4OWL-0eDZ6l21FMA94xuQhzfDCxLi7\",\"audience\":\"https://securityapp/\",\"grant_type\":\"client_credentials\"}"

headers = { 'content-type': "application/json" }

conn.request("POST", "/oauth/token", payload, headers)

res = conn.getresponse()
data = res.read()

print(data.decode("utf-8"))