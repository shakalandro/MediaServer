import socket

def recieve(data):
    offset = ""
    quality = "512"
    vcodec = ""
    port = "3000"
    mux = "ps"
    ip = socket.gethostbyname_ex(socket.gethostname())[2][0]
    if 'host' in data:
        host = data['host']
    if 'video' in data:
        extension = data['video']
    if 'offset' in data:
        offset =  handle_offset(data['offset'])
    if 'quality' in data:
        quality = handle_quality(data['quality'])
    transcode = "#transcode{vcodec=" + vcodec + ",vb=" + quality + "}"
    standard = "#standard{mux=" + mux + ",dst=" + ip + ":" + port + ",access=http}"
    return "vlc -vvv " + data['video'] + " -I rc " + offset + "--sout \'" + standard + "\'" 

def handle_offset(offset):
    return "--start-time " + offset + " "

def handle_quality(quality):    
    if quality is 'low':
        return "128"
    if quality is 'medium':
        return "512"
    if quality is 'high':
        return "2048"
    
tel = {'video' : 'SharkTales.ogv'}
print(recieve(tel))
