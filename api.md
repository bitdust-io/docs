# BitDust API


* [Intro](#intro)
* [Access](#access)
* [API methods](#api-methods)


## Intro

Make sure your BitDust engine process is already running on that machine first.

There are multiple ways you can interract with the BitDust engine main process.
Here you can find some examples of how to do that using different clients.



#### HTTP Rest API

The API server inside the engine is running on `localhost:8180` by default.
This can be modified via program settings.

You can use `curl` command to execute HTTP calls directly:

    curl -X GET -H 'api_secret:abc' 'localhost:8180/process/health/v1'
    {
      "execution": "0.000107",
      "status": "OK"
    }



#### WebSocket

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



#### Command line shell client

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




#### process\_stop()

Stop the main process immediately.

###### HTTP
    curl -X GET 'localhost:8180/process/stop/v1'

###### WebSocket
    websocket.send('{"command": "api_call", "method": "process_stop", "kwargs": {} }');


#### process\_restart()

Restart the main process.

###### HTTP
    curl -X GET 'localhost:8180/process/restart/v1'

###### WebSocket
    websocket.send('{"command": "api_call", "method": "process_restart", "kwargs": {} }');


#### process\_health()

Returns positive response if engine process is running. This method suppose to be used for health checks.

###### HTTP
    curl -X GET 'localhost:8180/process/health/v1'

###### WebSocket
    websocket.send('{"command": "api_call", "method": "process_health", "kwargs": {} }');


#### process\_debug()

Execute a breakpoint inside the main thread and start Python shell using standard `pdb.set_trace()` debugger method.

This is only useful if you already have executed the BitDust engine manually via shell console and would like
to interrupt it and investigate things.

This call will block the main process and it will stop responding to any API calls.

###### HTTP
    curl -X GET 'localhost:8180/process/debug/v1'

###### WebSocket
    websocket.send('{"command": "api_call", "method": "process_debug", "kwargs": {} }');


#### config\_get(key)

Returns current key/value from the program settings.

###### HTTP
    curl -X GET 'localhost:8180/config/get/v1?key=logs/debug-level'

###### WebSocket
    websocket.send('{"command": "api_call", "method": "config_get", "kwargs": {"key": "logs/debug-level"} }');


#### config\_set(key, value)

Set a value for given key option.

###### HTTP
    curl -X POST 'localhost:8180/config/set/v1' -d '{"key": "logs/debug-level", "value": 12}'

###### WebSocket
    websocket.send('{"command": "api_call", "method": "config_set", "kwargs": {"key": "logs/debug-level", "value": 12} }');


#### configs\_list(sort=False)

Provide detailed info about all program settings.

###### HTTP
    curl -X GET 'localhost:8180/config/list/v1'

###### WebSocket
    websocket.send('{"command": "api_call", "method": "configs_list", "kwargs": {} }');


#### configs\_tree()

Returns all options as a tree structure, can be more suitable for UI operations.

###### HTTP
    curl -X GET 'localhost:8180/config/tree/v1'

###### WebSocket
    websocket.send('{"command": "api_call", "method": "configs_tree", "kwargs": {} }');


#### identity\_get(include\_xml\_source=False)

Returns your identity info.

###### HTTP
    curl -X GET 'localhost:8180/identity/get/v1'

###### WebSocket
    websocket.send('{"command": "api_call", "method": "identity_get", "kwargs": {} }');


#### identity\_create(username, preferred\_servers=[])

Generates new private key and creates new identity for you to be able to communicate with other nodes in the network.

Parameter `username` defines filename of the new identity.

###### HTTP
    curl -X POST 'localhost:8180/identity/create/v1' -d '{"username": "alice"}'

###### WebSocket
    websocket.send('{"command": "api_call", "method": "identity_create", "kwargs": {"username": "alice"} }');


#### identity\_backup(destination\_filepath)

Creates local file at `destination_filepath` on your disk drive with a backup copy of your private key and recent IDURL.

You can use that file to restore identity in case of lost data using `identity_recover()` API method.

WARNING! Make sure to always have a backup copy of your identity secret key in a safe place - there is no other way
to restore your data in case of lost.

###### HTTP
    curl -X POST 'localhost:8180/identity/backup/v1' -d '{"destination_filepath": "/tmp/alice_backup.key"}'

###### WebSocket
    websocket.send('{"command": "api_call", "method": "identity_backup", "kwargs": {"destination_filepath": "/tmp/alice_backup.key"} }');


#### identity\_recover(private\_key\_source, known\_idurl=None)

Restores your identity from backup copy.

Input parameter `private_key_source` must contain your latest IDURL and the private key as openssh formated string.

###### HTTP
    curl -X POST 'localhost:8180/identity/recover/v1' -d '{"private_key_source": "http://some-host.com/alice.xml\n-----BEGIN RSA PRIVATE KEY-----\nMIIEogIBAAKC..."}'

###### WebSocket
    websocket.send('{"command": "api_call", "method": "identity_recover", "kwargs": {"private_key_source": "http://some-host.com/alice.xml\n-----BEGIN RSA PRIVATE KEY-----\nMIIEogIBAAKC..."} }');


#### identity\_erase(erase\_private\_key=False)

Method will erase current identity file and the private key (optionally).
All network services will be stopped first.

###### HTTP
    curl -X DELETE 'localhost:8180/identity/erase/v1' -d '{"erase_private_key": true}'

###### WebSocket
    websocket.send('{"command": "api_call", "method": "identity_erase", "kwargs": {"erase_private_key": true} }');


#### identity\_rotate()

Rotate your identity sources and republish identity file on another ID server even if current ID servers are healthy.

Normally that procedure is executed automatically when current process detects unhealthy ID server among your identity sources.

This method is provided for testing and development purposes.

###### HTTP
    curl -X PUT 'localhost:8180/identity/rotate/v1'

###### WebSocket
    websocket.send('{"command": "api_call", "method": "identity_rotate", "kwargs": {} }');


#### identity\_cache\_list()

Returns list of all cached locally identity files received from other users.

###### HTTP
    curl -X GET 'localhost:8180/identity/cache/list/v1'

###### WebSocket
    websocket.send('{"command": "api_call", "method": "identity_cache_list", "kwargs": {} }');


#### key\_get(key\_id, include\_private=False)

Returns details of the registered public or private key.

Use `include_private=True` if you also need a private key (as openssh formated string) to be present in the response.

###### HTTP
    curl -X GET 'localhost:8180/key/get/v1?key_id=abcd1234$alice@server-a.com'

###### WebSocket
    websocket.send('{"command": "api_call", "method": "key_get", "kwargs": {"key_id": "abcd1234$alice@server-a.com"} }');


#### keys\_list(sort=False, include\_private=False)

List details for all registered public and private keys.

Use `include_private=True` if you also need a private key (as openssh formated string) to be present in the response.

###### HTTP
    curl -X GET 'localhost:8180/key/list/v1?include_private=1'

###### WebSocket
    websocket.send('{"command": "api_call", "method": "keys_list", "kwargs": {"include_private": 1} }');


#### key\_create(key\_alias, key\_size=None, label="", include\_private=False)

Generate new RSA private key and add it to the list of registered keys with a new `key_id`.

Optional input parameter `key_size` can be 1024, 2048, 4096. If `key_size` was not passed, default value will be
populated from the `personal/private-key-size` program setting.

Parameter `label` can be used to attach some meaningful information for the user to display in the UI.

Use `include_private=True` if you also need a private key (as openssh formated string) to be present in the response.

###### HTTP
    curl -X POST 'localhost:8180/key/create/v1' -d '{"key_alias": "abcd1234", "key_size": 1024, "label": "Cats and Dogs"}'

###### WebSocket
    websocket.send('{"command": "api_call", "method": "key_create", "kwargs": {"key_alias": "abcd1234", "key_size": 1024, "label": "Cats and Dogs"} }');


#### key\_label(key\_id, label)

Set new label for the given key.

###### HTTP
    curl -X POST 'localhost:8180/key/label/v1' -d '{"key_id": "abcd1234$alice@server-a.com", "label": "Man and Woman"}'

###### WebSocket
    websocket.send('{"command": "api_call", "method": "key_label", "kwargs": {"key_id": "abcd1234$alice@server-a.com", "label": "Man and Woman"} }');


#### key\_erase(key\_id)

Unregister and remove given key from the list of known keys and erase local file.

###### HTTP
    curl -X DELETE 'localhost:8180/key/erase/v1' -d '{"key_id": "abcd1234$alice@server-a.com"}'

###### WebSocket
    websocket.send('{"command": "api_call", "method": "key_erase", "kwargs": {"key_id": "abcd1234$alice@server-a.com"} }');


#### key\_share(key\_id, trusted\_user\_id, include\_private=False, timeout=10)

Connects to remote user and transfer given public or private key to that node.
This way you can share access to files/groups/resources with other users in the network.

If you pass `include_private=True` also private part of the key will be shared, otherwise only public part.

###### HTTP
    curl -X PUT 'localhost:8180/key/share/v1' -d '{"key_id": "abcd1234$alice@server-a.com", "trusted_user_id": "bob@machine-b.net"}'

###### WebSocket
    websocket.send('{"command": "api_call", "method": "key_share", "kwargs": {"key_id": "abcd1234$alice@server-a.com", "trusted_user_id": "bob@machine-b.net"} }');


#### key\_audit(key\_id, untrusted\_user\_id, is\_private=False, timeout=10)

Connects to remote node identified by `untrusted_user_id` parameter and request audit of given public or private key `key_id` on that node.

Returns positive result if audit process succeed - that means remote user really possess the key.

###### HTTP
    curl -X POST 'localhost:8180/key/audit/v1' -d '{"key_id": "abcd1234$alice@server-a.com", "untrusted_user_id": "carol@computer-c.net", "is_private": 1}'

###### WebSocket
    websocket.send('{"command": "api_call", "method": "key_audit", "kwargs": {"key_id": "abcd1234$alice@server-a.com", "untrusted_user_id": "carol@computer-c.net", "is_private": 1} }');


#### files\_sync()

This should re-start "data synchronization" process with your remote suppliers.

Normally all communications and synchronizations are handled automatically, so you do not need to
call that method.

This method is provided for testing and development purposes.

###### HTTP
    curl -X GET 'localhost:8180/file/sync/v1'

###### WebSocket
    websocket.send('{"command": "api_call", "method": "files_sync", "kwargs": {} }');


#### file\_exists(remote\_path)

Returns positive result if file or folder with such `remote_path` already exists in the catalog.

###### HTTP
    curl -X GET 'localhost:8180/file/exists/v1?remote_path=abcd1234$alice@server-a.com:pictures/cats/pussy.png'

###### WebSocket
    websocket.send('{"command": "api_call", "method": "file_exists", "kwargs": {"remote_path": "abcd1234$alice@server-a.com:pictures/cats/pussy.png"} }');


#### file\_info(remote\_path, include\_uploads=True, include\_downloads=True)

Returns detailed info about given file or folder in the catalog.

You can also use `include_uploads` and `include_downloads` parameters to get more info about currently running
uploads and downloads.

###### HTTP
    curl -X GET 'localhost:8180/file/info/v1?remote_path=abcd1234$alice@server-a.com:pictures/dogs/bobby.jpeg'

###### WebSocket
    websocket.send('{"command": "api_call", "method": "file_info", "kwargs": {"remote_path": "abcd1234$alice@server-a.com:pictures/dogs/bobby.jpeg"} }');


#### file\_create(remote\_path, as\_folder=False, exist\_ok=False, force\_path\_id=None)

Creates new file in the catalog, but do not upload any data to the network yet.

This method only creates a "virtual ID" for the new data.

Pass `as_folder=True` to create a virtual folder instead of a file.

###### HTTP
    curl -X POST 'localhost:8180/file/create/v1' -d '{"remote_path": "abcd1234$alice@server-a.com:movies/travels/safari.mp4"}'

###### WebSocket
    websocket.send('{"command": "api_call", "method": "file_create", "kwargs": {"remote_path": "abcd1234$alice@server-a.com:movies/travels/safari.mp4"} }');


#### file\_delete(remote\_path)

Removes virtual file or folder from the catalog and also notifies your remote suppliers to clean up corresponding uploaded data.

###### HTTP
    curl -X POST 'localhost:8180/file/delete/v1' -d '{"remote_path": "abcd1234$alice@server-a.com:cars/ferrari.gif"}'

###### WebSocket
    websocket.send('{"command": "api_call", "method": "file_delete", "kwargs": {"remote_path": "abcd1234$alice@server-a.com:cars/ferrari.gif"} }');


#### files\_uploads(include\_running=True, include\_pending=True)

Returns a list of currently running uploads and list of pending items to be uploaded.

###### HTTP
    curl -X GET 'localhost:8180/file/upload/v1'

###### WebSocket
    websocket.send('{"command": "api_call", "method": "files_uploads", "kwargs": {} }');


#### file\_upload\_start(local\_path, remote\_path, wait\_result=False, open\_share=False)

Starts a new file or folder (including all sub-folders and files) upload from `local_path` on your disk drive
to the virtual location `remote_path` in the catalog. New "version" of the data will be created for given catalog item
and uploading task started.

You can use `wait_result=True` to block the response from that method until uploading finishes or fails (makes no sense for large uploads).

Parameter `open_share` can be useful if you uploading data into a "shared" virtual path using another key that shared to you.

###### HTTP
    curl -X POST 'localhost:8180/file/upload/start/v1' -d '{"remote_path": "abcd1234$alice@server-a.com:cars/fiat.jpeg", "local_path": "/tmp/fiat.jpeg"}'

###### WebSocket
    websocket.send('{"command": "api_call", "method": "file_upload_start", "kwargs": {"remote_path": "abcd1234$alice@server-a.com:cars/fiat.jpeg", "local_path": "/tmp/fiat.jpeg"} }');


#### file\_upload\_stop(remote\_path)

Useful method if you need to interrupt and cancel already running uploading task.

###### HTTP
    curl -X POST 'localhost:8180/file/upload/stop/v1' -d '{"remote_path": "abcd1234$alice@server-a.com:cars/fiat.jpeg"}'

###### WebSocket
    websocket.send('{"command": "api_call", "method": "file_upload_stop", "kwargs": {"remote_path": "abcd1234$alice@server-a.com:cars/fiat.jpeg"} }');


#### files\_downloads()

Returns a list of currently running downloading tasks.

###### HTTP
    curl -X GET 'localhost:8180/file/download/v1'

###### WebSocket
    websocket.send('{"command": "api_call", "method": "files_downloads", "kwargs": {} }');


#### file\_download\_start(remote\_path, destination\_path=None, wait\_result=False, open\_share=True)

Download data from remote suppliers to your local machine.

You can use different methods to select the target data with `remote_path` input:

  + "virtual" path of the file
  + internal path ID in the catalog
  + full data version identifier with path ID and version name

It is possible to select the destination folder to extract requested files to.
By default this method uses specified value from `paths/restore` program setting or user home folder.

You can use `wait_result=True` to block the response from that method until downloading finishes or fails (makes no sense for large files).

WARNING! Your existing local data in `destination_path` will be overwritten!

###### HTTP
    curl -X POST 'localhost:8180/file/download/start/v1' -d '{"remote_path": "abcd1234$alice@server-a.com:movies/back_to_the_future.mp4", "local_path": "/tmp/films/"}'

###### WebSocket
    websocket.send('{"command": "api_call", "method": "file_download_start", "kwargs": {"remote_path": "abcd1234$alice@server-a.com:movies/back_to_the_future.mp4", "local_path": "/tmp/films/"} }');


#### file\_download\_stop(remote\_path)

Abort currently running restore process.

###### HTTP
    curl -X POST 'localhost:8180/file/download/stop/v1' -d '{"remote_path": "abcd1234$alice@server-a.com:cars/fiat.jpeg"}'

###### WebSocket
    websocket.send('{"command": "api_call", "method": "file_download_stop", "kwargs": {"remote_path": "abcd1234$alice@server-a.com:cars/fiat.jpeg"} }');


#### file\_explore(local\_path)

Useful method to be executed from the UI right after downloading is finished.

It will open default OS file manager and display
given `local_path` to the user so he can do something with the file.

###### HTTP
    curl -X GET 'localhost:8180/file/explore/v1?local_path=/tmp/movies/back_to_the_future.mp4'

###### WebSocket
    websocket.send('{"command": "api_call", "method": "file_explore", "kwargs": {"local_path": "/tmp/movies/back_to_the_future.mp4"} }');


#### shares\_list(only\_active=False, include\_mine=True, include\_granted=True)

Returns a list of registered "shares" - encrypted locations where you can upload/download files.

Use `only_active=True` to select only connected shares.

Parameters `include_mine` and `include_granted` can be used to filter shares created by you,
or by other users that shared a key with you before.

###### HTTP
    curl -X GET 'localhost:8180/share/list/v1?only_active=1'

###### WebSocket
    websocket.send('{"command": "api_call", "method": "shares_list", "kwargs": {"only_active": 1} }');


#### share\_create(owner\_id=None, key\_size=None, label="")

Creates a new "share" - virtual location where you or other users can upload/download files.

This method generates a new RSA private key that will be used to encrypt and decrypt files belongs to that share.

By default you are the owner of the new share and uploaded files will be stored by your suppliers.
You can also use `owner_id` parameter if you wish to set another owner for that new share location.
In that case files will be stored not on your suppliers but on his/her suppliers, if another user authorized the share.

Optional input parameter `key_size` can be 1024, 2048, 4096. If `key_size` was not passed, default value will be
populated from the `personal/private-key-size` program setting.

Parameter `label` can be used to attach some meaningful information about that share location.

###### HTTP
    curl -X POST 'localhost:8180/share/create/v1' -d '{"label": "my summer holidays"}'

###### WebSocket
    websocket.send('{"command": "api_call", "method": "share_create", "kwargs": {"label": "my summer holidays"} }');


#### share\_delete(key\_id)

Stop the active share identified by the `key_id` and erase the private key.

###### HTTP
    curl -X DELETE 'localhost:8180/share/delete/v1' -d '{"key_id": "share_7e9726e2dccf9ebe6077070e98e78082$alice@server-a.com"}'

###### WebSocket
    websocket.send('{"command": "api_call", "method": "share_delete", "kwargs": {"key_id": "share_7e9726e2dccf9ebe6077070e98e78082$alice@server-a.com"} }');


#### share\_grant(key\_id, trusted\_user\_id, timeout=30)

Provide access to given share identified by `key_id` to another trusted user.

This method will transfer private key to remote user `trusted_user_id` and you both will be
able to upload/download file to the shared location.

###### HTTP
    curl -X PUT 'localhost:8180/share/grant/v1' -d '{"key_id": "share_7e9726e2dccf9ebe6077070e98e78082$alice@server-a.com", "trusted_user_id": "bob@machine-b.net"}'

###### WebSocket
    websocket.send('{"command": "api_call", "method": "share_grant", "kwargs": {"key_id": "share_7e9726e2dccf9ebe6077070e98e78082$alice@server-a.com", "trusted_user_id": "bob@machine-b.net"} }');


#### share\_open(key\_id)

Activates given share and initiate required connections to remote suppliers to make possible to upload and download shared files.

###### HTTP
    curl -X PUT 'localhost:8180/share/open/v1' -d '{"key_id": "share_7e9726e2dccf9ebe6077070e98e78082$alice@server-a.com"}'

###### WebSocket
    websocket.send('{"command": "api_call", "method": "share_open", "kwargs": {"key_id": "share_7e9726e2dccf9ebe6077070e98e78082$alice@server-a.com"} }');


#### share\_close(key\_id)

Disconnects and deactivate given share location.

###### HTTP
    curl -X PUT 'localhost:8180/share/close/v1' -d '{"key_id": "share_7e9726e2dccf9ebe6077070e98e78082$alice@server-a.com"}'

###### WebSocket
    websocket.send('{"command": "api_call", "method": "share_close", "kwargs": {"key_id": "share_7e9726e2dccf9ebe6077070e98e78082$alice@server-a.com"} }');


#### share\_history()

Method is not implemented yet.


#### groups\_list(only\_active=False, include\_mine=True, include\_granted=True)

Returns a list of registered message groups.

Use `only_active=True` to select only connected and active groups.

Parameters `include_mine` and `include_granted` can be used to filter groups created by you,
or by other users that shared a key with you before.

###### HTTP
    curl -X GET 'localhost:8180/group/list/v1'

###### WebSocket
    websocket.send('{"command": "api_call", "method": "groups_list", "kwargs": {} }');


#### group\_create(creator\_id=None, key\_size=None, label="")

Creates a new messaging group.

This method generates a new RSA private key that will be used to encrypt and decrypt messages streamed thru that group.

Optional input parameter `key_size` can be 1024, 2048, 4096. If `key_size` was not passed, default value will be
populated from the `personal/private-key-size` program setting.

Parameter `label` can be used to attach some meaningful information about that group.

###### HTTP
    curl -X POST 'localhost:8180/group/create/v1' -d '{"label": "chat with my friends"}'

###### WebSocket
    websocket.send('{"command": "api_call", "method": "group_create", "kwargs": {"label": "chat with my friends"} }');


#### group\_info(group\_key\_id)

Returns detailed info about the message group identified by `group_key_id`.

###### HTTP
    curl -X GET 'localhost:8180/group/info/v1?group_key_id=group_95d0fedc46308e2254477fcb96364af9$alice@server-a.com'

###### WebSocket
    websocket.send('{"command": "api_call", "method": "group_info", "kwargs": {"group_key_id": "group_95d0fedc46308e2254477fcb96364af9$alice@server-a.com"} }');


#### group\_join(group\_key\_id)

Activates given messaging group to be able to receive streamed messages or send a new message to the group.

###### HTTP
    curl -X POST 'localhost:8180/group/join/v1' -d '{"group_key_id": "group_95d0fedc46308e2254477fcb96364af9$alice@server-a.com"}'

###### WebSocket
    websocket.send('{"command": "api_call", "method": "group_join", "kwargs": {"group_key_id": "group_95d0fedc46308e2254477fcb96364af9$alice@server-a.com"} }');


#### group\_leave(group\_key\_id, erase\_key=False)

Deactivates given messaging group. If `erase_key=True` will also erase the private key related to that group.

###### HTTP
    curl -X DELETE 'localhost:8180/group/leave/v1' -d '{"group_key_id": "group_95d0fedc46308e2254477fcb96364af9$alice@server-a.com"}'

###### WebSocket
    websocket.send('{"command": "api_call", "method": "group_leave", "kwargs": {"group_key_id": "group_95d0fedc46308e2254477fcb96364af9$alice@server-a.com"} }');


#### group\_share(group\_key\_id, trusted\_user\_id, timeout=30)

Provide access to given group identified by `group_key_id` to another trusted user.

This method will transfer private key to remote user `trusted_user_id` inviting him to the messaging group.

###### HTTP
    curl -X PUT 'localhost:8180/group/share/v1' -d '{"group_key_id": "group_95d0fedc46308e2254477fcb96364af9$alice@server-a.com", "trusted_user_id": "bob@machine-b.net"}'

###### WebSocket
    websocket.send('{"command": "api_call", "method": "group_share", "kwargs": {"key_id": "group_95d0fedc46308e2254477fcb96364af9$alice@server-a.com", "trusted_user_id": "bob@machine-b.net"} }');


#### friends\_list()

Returns list of registered correspondents.

###### HTTP
    curl -X GET 'localhost:8180/friend/list/v1'

###### WebSocket
    websocket.send('{"command": "api_call", "method": "friends_list", "kwargs": {} }');


#### friend\_add(trusted\_user\_id, alias="")

Add user to the list of correspondents.

You can attach an alias to that user as a label to be displayed in the UI.

###### HTTP
    curl -X POST 'localhost:8180/friend/add/v1' -d '{"trusted_user_id": "dave@device-d.gov", "alias": "SuperMario"}'

###### WebSocket
    websocket.send('{"command": "api_call", "method": "friend_add", "kwargs": {"trusted_user_id": "dave@device-d.gov", "alias": "SuperMario"} }');


#### friend\_remove(user\_id)

Removes given user from the list of correspondents.

###### HTTP
    curl -X DELETE 'localhost:8180/friend/add/v1' -d '{"user_id": "dave@device-d.gov"}'

###### WebSocket
    websocket.send('{"command": "api_call", "method": "friend_add", "kwargs": {"user_id": "dave@device-d.gov"} }');


#### user\_ping(user\_id, timeout=15, retries=2)

Sends `Identity` packet to remote peer and wait for an `Ack` packet to check connection status.

Method can be used to check and verify that remote node is on-line at the moment (if you are also on-line).

###### HTTP
    curl -X GET 'localhost:8180/user/ping/v1?user_id=carol@computer-c.net'

###### WebSocket
    websocket.send('{"command": "api_call", "method": "suppliers_ping", "kwargs": {} }');


#### user\_status(user\_id)

Returns short info about current on-line status of the given user.

###### HTTP
    curl -X GET 'localhost:8180/user/status/v1?user_id=carol@computer-c.net'

###### WebSocket
    websocket.send('{"command": "api_call", "method": "user_status", "kwargs": {"user_id": "carol@computer-c.net"} }');


#### user\_status\_check(user\_id, timeout=5)

Returns current online status of a user and only if node is known but disconnected performs "ping" operation.

###### HTTP
    curl -X GET 'localhost:8180/user/status/check/v1?user_id=carol@computer-c.net'

###### WebSocket
    websocket.send('{"command": "api_call", "method": "user_status_check", "kwargs": {"user_id": "carol@computer-c.net"} }');


#### user\_search(nickname, attempts=1)

Doing lookup of a single `nickname` registered in the DHT network.

###### HTTP
    curl -X GET 'localhost:8180/user/search/v1?nickname=carol'

###### WebSocket
    websocket.send('{"command": "api_call", "method": "user_search", "kwargs": {"nickname": "carol"} }');


#### user\_observe(nickname, attempts=3)

Reads all records registered for given `nickname` in the DHT network.

It could be that multiple users chosen same nickname when creating an identity.

###### HTTP
    curl -X GET 'localhost:8180/user/observe/v1?nickname=carol'

###### WebSocket
    websocket.send('{"command": "api_call", "method": "user_observe", "kwargs": {"nickname": "carol"} }');


#### message\_history(recipient\_id=None, sender\_id=None, message\_type=None, offset=0, limit=100)

Returns chat history stored during communications with given user or messaging group.

###### HTTP
    curl -X GET 'localhost:8180/message/history/v1?message_type=group_message&recipient_id=group_95d0fedc46308e2254477fcb96364af9$alice@server-a.com'

###### WebSocket
    websocket.send('{"command": "api_call", "method": "message_history", "kwargs": {"recipient_id" : "group_95d0fedc46308e2254477fcb96364af9$alice@server-a.com", "message_type": "group_message"} }');


#### message\_send(recipient\_id, data, ping\_timeout=30, message\_ack\_timeout=15)

Sends a text message to remote peer, `recipient_id` is a string with a nickname, global_id or IDURL of the remote user.

###### HTTP
    curl -X POST 'localhost:8180/message/send/v1' -d '{"recipient_id": "carlos@computer-c.net", "data": {"message": "Hola Amigo!"}}'

###### WebSocket
    websocket.send('{"command": "api_call", "method": "message_send", "kwargs": {"recipient_id": "carlos@computer-c.net", "data": {"message": "Hola Amigos!"}} }');


#### message\_send\_group(group\_key\_id, data)

Sends a text message to a group of users.

###### HTTP
    curl -X POST 'localhost:8180/message/send/group/v1' -d '{"group_key_id": "group_95d0fedc46308e2254477fcb96364af9$alice@server-a.com", "data": {"message": "Hola Amigos!"}}' 

###### WebSocket
    websocket.send('{"command": "api_call", "method": "message_send_group", "kwargs": {"group_key_id": "group_95d0fedc46308e2254477fcb96364af9$alice@server-a.com", "data": {"message": "Hola Amigos!"}} }');


#### message\_receive(consumer\_callback\_id, direction="incoming", message\_types="private\_message,group\_message", polling\_timeout=60)

This method can be used by clients to listen and process streaming messages.

If there are no pending messages received yet in the stream, this method will block and will be waiting for any message to come.

If some messages are already waiting in the stream to be consumed method will return them immediately.
As soon as client received and processed the response messages are marked as "consumed" and released from the stream.

Client should call that method again to listen for next messages in the stream. You can use `polling_timeout` parameter
to control blocking for receiving duration. This is very similar to a long polling technique.

Once client stopped calling that method and do not "consume" messages anymor given `consumer_callback_id` will be dropped
after 100 non-collected messages.

You can set parameter `direction=outgoing` to only populate messages you are sending to others - can be useful for UI clients.

Also you can use parameter `message_types` to select only specific types of messages: "private_message" or "group_message".

This method is only make sense for HTTP interface, because using a WebSocket client will receive streamed message directly.

###### HTTP
    curl -X GET 'localhost:8180/message/receive/my-client-group-messages/v1?message_types=group_message'


#### suppliers\_list(customer\_id=None, verbose=False)

This method returns a list of your suppliers.
Those nodes stores your encrypted file or file uploaded by other users that still belongs to you.

Your BitDust node also sometimes need to connect to suppliers of other users to upload or download shared data.
Those external suppliers lists are cached and can be selected here with `customer_id` optional parameter.

###### HTTP
    curl -X GET 'localhost:8180/supplier/list/v1'

###### WebSocket
    websocket.send('{"command": "api_call", "method": "suppliers_list", "kwargs": {} }');


#### supplier\_change(position=None, supplier\_id=None, new\_supplier\_id=None)

The method will execute a fire/hire process for given supplier. You can specify which supplier to be replaced by position or ID.

If optional parameter `new_supplier_id` was not specified another random node will be found via DHT network and it will
replace the current supplier. Otherwise `new_supplier_id` must be an existing node in the network and
the process will try to connect and use that node as a new supplier.

As soon as new node is found and connected, rebuilding of all uploaded data will be automatically started and new supplier
will start getting reconstructed fragments of your data piece by piece.

###### HTTP
    curl -X POST 'localhost:8180/supplier/change/v1' -d '{"position": 1, "new_supplier_id": "carol@computer-c.net"}'

###### WebSocket
    websocket.send('{"command": "api_call", "method": "supplier_change", "kwargs": {"position": 1, "new_supplier_id": "carol@computer-c.net"} }');


#### suppliers\_ping()

Sends short requests to all suppliers to verify current connection status.

###### HTTP
    curl -X POST 'localhost:8180/supplier/ping/v1'

###### WebSocket
    websocket.send('{"command": "api_call", "method": "suppliers_ping", "kwargs": {} }');


#### suppliers\_dht\_lookup(customer\_id=None)

Scans DHT network for key-value pairs related to given customer and returns a list its suppliers.

###### HTTP
    curl -X GET 'localhost:8180/supplier/list/dht/v1?customer_id=alice@server-a.com'

###### WebSocket
    websocket.send('{"command": "api_call", "method": "suppliers_dht_lookup", "kwargs": {"customer_id": "alice@server-a.com"} }');


#### customers\_list(verbose=False)

Method returns list of your customers - nodes for whom you are storing data on that host.

###### HTTP
    curl -X GET 'localhost:8180/customer/list/v1'

###### WebSocket
    websocket.send('{"command": "api_call", "method": "customers_list", "kwargs": {} }');


#### customer\_reject(customer\_id)

Stop supporting given customer, remove all related files from local disc, close connections with that node.

###### HTTP
    curl -X DELETE 'localhost:8180/customer/reject/v1' -d '{"customer_id": "dave@device-d.gov"}'

###### WebSocket
    websocket.send('{"command": "api_call", "method": "customer_reject", "kwargs": {"customer_id": "dave@device-d.gov"} }');


#### customers\_ping()

Check current on-line status of all customers.

###### HTTP
    curl -X POST 'localhost:8180/customer/ping/v1'

###### WebSocket
    websocket.send('{"command": "api_call", "method": "customers_ping", "kwargs": {} }');


#### space\_donated()

Returns detailed info about quotas and usage of the storage space you donated to your customers.

###### HTTP
    curl -X GET 'localhost:8180/space/donated/v1'

###### WebSocket
    websocket.send('{"command": "api_call", "method": "space_donated", "kwargs": {} }');


#### space\_consumed()

Returns info about current usage of the storage space provided by your suppliers.

###### HTTP
    curl -X GET 'localhost:8180/space/consumed/v1'

###### WebSocket
    websocket.send('{"command": "api_call", "method": "space_consumed", "kwargs": {} }');


#### space\_local()

Returns info about current usage of your local disk drive.

###### HTTP
    curl -X GET 'localhost:8180/space/local/v1'

###### WebSocket
    websocket.send('{"command": "api_call", "method": "space_local", "kwargs": {} }');


#### services\_list(with\_configs=False)

Returns detailed info about all currently running network services.

Pass `with_configs=True` to also see current program settings values related to each service.

This is a very useful method when you need to investigate a problem in the software.

###### HTTP
    curl -X GET 'localhost:8180/service/list/v1?with_configs=1'

###### WebSocket
    websocket.send('{"command": "api_call", "method": "services_list", "kwargs": {"with_configs": 1} }');


#### service\_info(service\_name)

Returns detailed info about single service.

###### HTTP
    curl -X GET 'localhost:8180/service/info/service_private_groups/v1'

###### WebSocket
    websocket.send('{"command": "api_call", "method": "service_info", "kwargs": {"service_name": "service_private_groups"} }');


#### service\_start(service\_name)

Starts given service immediately.

This method also set `True` for correspondent option in the program settings to mark the service as enabled:

    .bitdust/config/services/[service name]/enabled

Other dependent services, if they were enabled before but stopped, also will be started.

###### HTTP
    curl -X POST 'localhost:8180/service/start/service_supplier/v1'

###### WebSocket
    websocket.send('{"command": "api_call", "method": "service_start", "kwargs": {"service_name": "service_supplier"} }');


#### service\_stop(service\_name)

Stop given service immediately.

This method also set `False` for correspondent option in the program settings to mark the service as disabled:

    .bitdust/config/services/[service name]/enabled

Dependent services will be stopped as well but will not be disabled.

###### HTTP
    curl -X POST 'localhost:8180/service/stop/service_supplier/v1'

###### WebSocket
    websocket.send('{"command": "api_call", "method": "service_stop", "kwargs": {"service_name": "service_supplier"} }');


#### service\_restart(service\_name, wait\_timeout=10)

This method will stop given service and start it again, but only if it is already enabled.
It will not modify corresponding option for that service in the program settings.

All dependent services will be restarted as well.

Very useful method when you need to reload some parts of the application without full process restart.

###### HTTP
    curl -X POST 'localhost:8180/service/restart/service_customer/v1'

###### WebSocket
    websocket.send('{"command": "api_call", "method": "service_restart", "kwargs": {"service_name": "service_customer"} }');


#### packets\_list()

Returns list of incoming and outgoing signed packets running at the moment.

###### HTTP
    curl -X GET 'localhost:8180/packet/list/v1'

###### WebSocket
    websocket.send('{"command": "api_call", "method": "packets_list", "kwargs": {} }');


#### packets\_stats()

Returns detailed info about overall network usage.

###### HTTP
    curl -X GET 'localhost:8180/packet/stats/v1'

###### WebSocket
    websocket.send('{"command": "api_call", "method": "packets_stats", "kwargs": {} }');


#### transfers\_list()

Returns list of current data fragments transfers to/from suppliers.

###### HTTP
    curl -X GET 'localhost:8180/transfer/list/v1'

###### WebSocket
    websocket.send('{"command": "api_call", "method": "transfers_list", "kwargs": {} }');


#### connections\_list(protocols=None)

Returns list of opened/active network connections.

Argument `protocols` can be used to select which protocols to be present in the response:

###### HTTP
    curl -X GET 'localhost:8180/connection/list/v1?protocols=tcp,udp,proxy'

###### WebSocket
    websocket.send('{"command": "api_call", "method": "connections_list", "kwargs": {"protocols": ["tcp", "udp", "proxy"]} }');


#### streams\_list(protocols=None)

Returns list of running streams of data fragments with recent upload/download progress percentage.

###### HTTP
    curl -X GET 'localhost:8180/stream/list/v1'

###### WebSocket
    websocket.send('{"command": "api_call", "method": "streams_list", "kwargs": {} }');


#### queues\_list()

Returns list of registered streaming queues.

###### HTTP
    curl -X GET 'localhost:8180/queue/list/v1'

###### WebSocket
    websocket.send('{"command": "api_call", "method": "queues_list", "kwargs": {} }');


#### queue\_consumers\_list()

Returns list of registered queue consumers.

###### HTTP
    curl -X GET 'localhost:8180/queue/consumer/list/v1'

###### WebSocket
    websocket.send('{"command": "api_call", "method": "queue_consumers_list", "kwargs": {} }');


#### queue\_producers\_list()

Returns list of registered queue producers.

###### HTTP
    curl -X GET 'localhost:8180/queue/producer/list/v1'

###### WebSocket
    websocket.send('{"command": "api_call", "method": "queue_producers_list", "kwargs": {} }');


#### event\_send(event\_id, data=None)

Method will generate and inject a new event inside the main process.

This method is provided for testing and development purposes.

###### HTTP
    curl -X POST 'localhost:8180/event/send/client-event-abc/v1' -d '{"data": {"some_key": "some_value"}}'

###### WebSocket
    websocket.send('{"command": "api_call", "method": "event_send", "kwargs": {"event_id": "client-event-produced", "data": {"some_key": "some_value"}} }');


#### event\_listen(consumer\_callback\_id)

This method can be used by clients to listen and process all events fired inside the main process.

If there are no pending events fired yet, this method will block and will be waiting for any new event.

If some messages are already waiting in the stream to be consumed method will return them immediately.
As soon as client received and processed the response events are marked as "consumed" and released from the buffer.

Client should call that method again to listen for next events. This is very similar to a long polling technique.

This method is only make sense for HTTP interface, because using a WebSocket client will receive application events directly.

###### HTTP
    curl -X GET 'localhost:8180/event/listen/my-client-event-hook/v1'



#### network\_stun(udp\_port=None, dht\_port=None)

Begins network STUN process to detect your network configuration and current external IP address of that host. 

###### HTTP
    curl -X GET 'localhost:8180/network/stun/v1'

###### WebSocket
    websocket.send('{"command": "api_call", "method": "network_stun", "kwargs": {} }');


#### network\_reconnect()

Method can be used to refresh network status and restart all internal connections.

###### HTTP
    curl -X GET 'localhost:8180/network/reconnect/v1'

###### WebSocket
    websocket.send('{"command": "api_call", "method": "network_reconnect", "kwargs": {} }');


#### network\_connected(wait\_timeout=5)

Method can be used by clients to ensure BitDust application is connected to other nodes in the network.

If all is good this method will block for `wait_timeout` seconds. In case of some network issues method will return result immediately.

###### HTTP
    curl -X GET 'localhost:8180/network/connected/v1'

###### WebSocket
    websocket.send('{"command": "api_call", "method": "network_connected", "kwargs": {} }');


#### network\_configuration()

Returns details about network services.

###### HTTP
    curl -X GET 'localhost:8180/network/configuration/v1'

###### WebSocket
    websocket.send('{"command": "api_call", "method": "network_configuration", "kwargs": {} }');


#### dht\_node\_find(node\_id\_64=None, layer\_id=0)

Lookup "closest" (in terms of hashes and cryptography) DHT nodes to a given `node_id_64` value.

Method can be also used to pick a random DHT node from the network if you do not pass any value to `node_id_64`.

Parameter `layer_id` specifies which layer of the routing table to be used.

###### HTTP
    curl -X GET 'localhost:8180/dht/node/find/v1?node_id_64=4271c8f079695d77f80186ac9365e3df949ff74d'

###### WebSocket
    websocket.send('{"command": "api_call", "method": "dht_node_find", "kwargs": {"node_id_64": "4271c8f079695d77f80186ac9365e3df949ff74d"} }');


#### dht\_user\_random(layer\_id=0, count=1)

Pick random live nodes from BitDust network.

Method is used during services discovery, for example when you need to hire a new supplier to store your data.

Parameter `layer_id` specifies which layer of the routing table to be used.

###### HTTP
    curl -X GET 'localhost:8180/dht/user/random/v1?count=2&layer_id=2'

###### WebSocket
    websocket.send('{"command": "api_call", "method": "dht_node_find", "kwargs": {"count": 2, "layer_id": 2} }');


#### dht\_value\_get(key, record\_type="skip\_validation", layer\_id=0, use\_cache\_ttl=None)

Fetch single key/value record from DHT network.

###### HTTP
    curl -X GET 'localhost:8180/dht/value/get/v1?key=abcd'

###### WebSocket
    websocket.send('{"command": "api_call", "method": "dht_value_get", "kwargs": {"key": "abcd"} }');


#### dht\_value\_set(key, value, expire=None, record\_type="skip\_validation", layer\_id=0)

Writes given key/value record into DHT network. Input parameter `value` must be a JSON value.

###### HTTP
    curl -X POST 'localhost:8180/dht/value/set/v1' -d '{"key": "abcd", "value": {"text": "A-B-C-D"}}'

###### WebSocket
    websocket.send('{"command": "api_call", "method": "dht_value_set", "kwargs": {"key": "abcd", "value": {"text": "A-B-C-D"}} }');


#### dht\_local\_db\_dump()

Method used for testing purposes, returns full list of all key/values stored locally on that DHT node.

###### HTTP
    curl -X GET 'localhost:8180/dht/db/dump/v1'

###### WebSocket
    websocket.send('{"command": "api_call", "method": "dht_local_db_dump", "kwargs": {} }');


#### automats\_list()

Returns a list of all currently running state machines.

This is a very useful method when you need to investigate a problem in the software.

###### HTTP
    curl -X GET 'localhost:8180/automat/list/v1'

###### WebSocket
    websocket.send('{"command": "api_call", "method": "automats_list", "kwargs": {} }');




