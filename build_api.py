import re
import os
import sys

method_rexp = '^def\s+(\w+)\((.*?)\)\:$'

fin = open(sys.argv[1])
fout = open(sys.argv[2], 'w')
fout.write('''# BitDust API


* [Intro](#intro)
* [Access](#access)
* [API methods](#api-methods)


## Intro

Make sure your BitDust engine process is already running on that machine first.

There are multiple ways you can interract with the BitDust engine main process.
Here you can find some examples of how to do that using different clients.



##### HTTP Rest API

The API server inside the engine is running on `localhost:8180` by default.
This can be modified via program settings.

You can use `curl` command to execute HTTP calls directly:

    curl -X GET -H 'api_secret:abc' 'localhost:8180/process/health/v1'
    {
      "execution": "0.000107",
      "status": "OK"
    }



##### WebSocket

The WebSocket server inside the engine is running on `localhost:8280` by default.
This can be modified via program settings.

Here is a very basic example of a JavaScript WebSocket client call:

    var websocket = null;
    websocket = new WebSocket("ws://127.0.0.1:8280?api_secret=abc");
    websocket.binaryType = "arraybuffer";
    websocket.onopen = function() {
        websocket.send('{"command": "api_call", "method": "process_health", "kwargs": {} }');
    };
    websocket.onmessage = function(e) {
        if (typeof e.data == "string") {
            console.log("WebSocket message received: " + e.data);
        }
    };



##### Command line shell client

Command line client is actually also using HTTP Rest API interface to interact with the main process.

To get more details about how to use BitDust via command line type in your terminal shell:

    bitdust help



## Access

Both HTTP and WebSocket interfaces are only accepting connections from the local host. This is an intended restriction
to prevent any kind of access from outside of the host operation system to the main BitDust process.
This way BitDust do not require user to have any kind of credentials to access the application.

To block access to BitDust API interface for non-authorized local clients a secret API token was introduced.
That feature suppose to be enabled by default if you just installed the application for the first time.

To verify that secret token is in use you need to open the folder `.bitdust/metadata/` and
check if a file `.bitdust/metadata/apisecret` exists and is not empty.
The file contains base64-formatted random token which is generated automatically by the application.

Authorized clients running on same operating system such as UI client and command line shell client will read that file from the disk and be
able to access the API methods. Non-authorized local clients that do not have access to the host operating system
will not be able to access the API.



## API methods

You can find bellow a list of all API methods available at the moment.


\n\n''')

while True:
    line = fin.readline()
    if line == '':
        break
    r = re.match(method_rexp, line.strip())
    if not r:
        continue
    method = r.group(1)
    params = r.group(2)
    comment = ''
    if method.startswith('_'):
        continue
    if method in ['OK', 'RESULT', 'ERROR', 'on_api_result_prepared']:
        continue
    line = fin.readline()
    if line == '':
        break
    if line and (line.strip().startswith('"""') or line.strip().startswith("'''")):
        if line.count('"""') == 2 or line.count("'''") == 2:
            comment = line.strip('"""').strip("'''").replace('"""','').replace("'''",'').replace('    ', '', 1)
        else:
            comment = line.replace('    ', '', 1)
            while True:
                line = fin.readline()
                if line == '':
                    break
                comment += line.replace('    ', '', 1)
                if line.count('"""') or line.count("'''"):
                    break
            comment = comment.strip('"""').strip("'''").replace('"""','').replace("'''",'')
    comment = comment.replace('Return:', '\n\n')
    # print '%s(%s)' % (method, params)
    sys.stdout.write('.')
    fout.write('#### %s(%s)\n' % (method.replace('_','\_'), params.replace('_','\_').replace("'", '"')))
    fout.write(('\n'.join(comment.splitlines())) + '\n\n')

sys.stdout.write('\n')

fout.write('\n\n')
fout.close()
fin.close()
