websocket = null;
function Connect(ip)
{
    ip = "ws://" + ip + ":8000/"
    websocket = new WebSocket(ip);
    websocket.onopen = function(evt){onOpen(evt)};
    websocket.onclose = function(evt){onClose(evt)};
    websocket.onerror = function(evt){onError(evt)};
    websocket.onmessage = function(evt){onMessage(evt)};
}


function onOpen(evt)
{
    console.log("Successful Connection");
}

function onClose(evt)
{
    console.log("Connection closed with code: " + evt.code);
}

function onMessage(evt)
{
    console.log("Got data" + evt.data);
    data = decodeJson(evt.data);
}

function onError(evt)
{
    
}

function Put(key, value, type)
{
    if(websocket != null)
    {
        websocket.send("PUT " + key + " " + value + " " + type);
        console.log("Put key: " + key + " value: " + value);
    }
}

function Get(key)
{
    if(websocket != null)
    {
        websocket.send("GET " + key);
    }
}