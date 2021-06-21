# RTSPStream_OpenCV
1.	// To stream local video using rtsp in container.
`docker build -t {tagname} .` <br>
`docker run {tagname}` <br>

2.	// Expose an API. This api on calling listens to rtsp stream. Use postman or any other tool to call the api. 
`docker build -t {tagname} .` <br>
`docker run -d -p 127.0.0.1:9000:9000 {tagname} .` <br>

API Call- 
POST http://127.0.0.1:9000/streams
body--
{
    "rtsp": "rtsp://172.19.0.3:554/media/video.mkv"
}

Since the above two containers are running seperately and no communcation is established between the continers. 
so create a docker network and the two containers in same network so that videocapture can listen to the rtsp stream

`docker network create {networkName}` <br>
`docker network connect rtspnetwork {containerId}` // stream (docker conatiner ls) to get container id. <br>
`docker network inspect rtspnetwork {containerId}`// stream capture api <br>

I have added you to my storage account `opencvstorage585`, frames will be sent to that storage.

Additional commands
   `docker network inspect rtspnetwork {containerId}` // inspect network config details. <br>
`docker container ls` // view all running container details. <br>
`docker stop {containerId}` <br>
`docker logs {containerId} -f` // for following docker logs <br>

For local debugging rtsp stream run `docker run -d -p 127.0.0.1:554:554 {tagname} .` to stream in any media player.


Add azure blob details for storing the frames in to the blob in azureBlobHelper.py
