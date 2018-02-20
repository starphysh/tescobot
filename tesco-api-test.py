    ########### Python 3.2 #############
import http.client, urllib.request, urllib.parse, urllib.error, base64

headers = {
    # Request headers
    'Ocp-Apim-Subscription-Key': '692b96d7ae1a48ca805cf64411ffd840',
}

params = urllib.parse.urlencode({
})

print(params)

try:
    conn = http.client.HTTPSConnection('dev.tescolabs.com')
    conn.request("GET", "/grocery/products/?query=beans&offset=1&limit=3&%s" % params, "{body}", headers)
    response = conn.getresponse()
    data = response.read()
    print(data)
    conn.close()
except Exception as e:
    print("[Errno {0}] {1}".format(e.errno, e.strerror))

####################################