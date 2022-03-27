var mapPeers={};


const localVideo = document.querySelector('#local-video')
var localStream=new MediaStream()

const constraints = {
    'video':true, 
    'audio':true,
}
userMedia = navigator.mediaDevices.getUserMedia(constraints).then(stream=>{
    localStream = stream;
    localVideo.srcObject = localStream;
    localVideo.muted = true;
    console.log('load stream')
    localVideo.play()

    var videoTracks=stream.getVideoTracks()
    var audioTracks = stream.getAudioTracks()
    $('#mute-btn').each(function(){
        var btn = this
        $(btn).toggleClass('btn-off')

        $(this).on('click',function(e){
            console.log('click mute')
            console.log(`is ${audioTracks[0].enabled}`)
            if(audioTracks[0].enabled){
                v = $(btn).siblings('video')[0]
                v.muted=true
                
            }else{
                v = $(btn).siblings('video')[0]
                console.log(v)
                v.muted = false

            }
            audioTracks[0].enabled =!audioTracks[0].enabled

            $(btn).toggleClass('btn-off')
        })
    
    })
    $('#close-cam-btn').each(function(){
        var btn = this
        $(this).on('click',function(e){
            console.log('click cam')
            el = $(btn).siblings('video')
            console.log(el.videoTracks)
            videoTracks[0].enabled = !videoTracks[0].enabled
            $(this).toggleClass('btn-off')
            console.log(el)
        })
        
    
    })
}).catch(error =>{
    console.log('error accessing media devices' + error)
    $('#video-btn').attr('disabled','true')
})

function createOfferer(peerUsername,receiver_channel_name){
    var peer = new RTCPeerConnection(null)
    addLocalTracks(peer)

    var dc = peer.createDataChannel('channel')
    dc.addEventListener('open',()=>{
        console.log('Connection opened!')
    })

    dc.addEventListener('message',dcOnMessage)
    var remoteVideo = createVideo(peerUsername)
    setOnTrack(peer,remoteVideo)

    mapPeers[peerUsername] = [peer,dc]
    peer.addEventListener('iceconnectionstatechange',()=>{
        var iceconnectionstate = peer.iceConnectionState
        if (iceconnectionstate === 'failed' || iceconnectionstate ==='disconnected' || iceconnectionstate==='closed'){
            delete mapPeers['peerUsername']

            if(iceconnectionstate != 'closed'){
                peer.close()
            }

            removeVideo(remoteVideo)
        }
    })

    peer.addEventListener('icecandidate',(event)=>{
        if(event.candidate){
            console.log('New ice candidate',JSON.stringify(peer.localDescription))
            return;
        }
        sendSignal('new-offer',{
            'sdp':peer.localDescription,
            'receiver_channel_name':receiver_channel_name
        })

    })

    peer.createOffer().then(o=> peer.setLocalDescription(o).then(()=>{
        console.log('local description set successfully')
    }))
}

function createAnswer(offer,peerUsername,receiver_channel_name){
    var peer = new RTCPeerConnection(null)
    addLocalTracks(peer)


    var remoteVideo = createVideo(peerUsername)
    setOnTrack(peer,remoteVideo)

    peer.addEventListener('datachannel',e=>{
        peer.dc = e.channel
        peer.dc.addEventListener('open',()=>{
            console.log('Connection opened!')
        })
        peer.dc.addEventListener('message',dcOnMessage);
        
        mapPeers[peerUsername] = [peer,peer.dc]
    })
    peer.addEventListener('iceconnectionstatechange',()=>{
        var iceconnectionstate = peer.iceConnectionState
        if (iceconnectionstate === 'failed' || iceconnectionstate ==='disconnected' || iceconnectionstate==='closed'){
            delete mapPeers['peerUsername']

            if(iceconnectionstate != 'closed'){
                peer.close()
            }

            removeVideo(remoteVideo)
        }
    })

    peer.addEventListener('icecandidate',(event)=>{
        if(event.candidate){
            console.log('New ice candidate',JSON.stringify(peer.localDescription))
            return;
        }
        sendSignal('new-answer',{
            'sdp':peer.localDescription,
            'receiver_channel_name':receiver_channel_name
        })
    })

    peer.setRemoteDescription(offer)
        .then(()=>{
            console.log('Remote description set successfully for %s',peerUsername);
            return peer.createAnswer();
        })
        .then(a =>{
            console.log('answer created')
            peer.setLocalDescription(a)
        })
}
function addLocalTracks(peer){
    localStream.getTracks().forEach(track =>{
        peer.addTrack(track,localStream)
    })
    return
}
function createVideo(peerUsername){
    var videoContainer = document.querySelector('#video-list-container')
    var remoteVideo = document.createElement("video")
    remoteVideo.classList.add('video-p2p')
    remoteVideo.id = peerUsername +'-video'
    remoteVideo.playsInline=true
    var videoWrapper = document.createElement('div')
    videoWrapper.classList.add('video-container')
    videoContainer.append(videoWrapper)
    videoWrapper.appendChild(remoteVideo)
    remoteVideo.muted=true
    remoteVideo.autoplay=true


    return remoteVideo
}
function setOnTrack(peer,remoteVideo){
    var remoteStream = new MediaStream()
    remoteVideo.srcObject = remoteStream
    peer.addEventListener('track', async(event)=>{
        remoteStream.addTrack(event.track,remoteStream)
    })

}
function removeVideo(remoteVideo){
    var wrapper = remoteVideo.parentNode;
    wrapper.parentNode.removeChild(wrapper)
}

function sendSignal(action,message){
    var jsonStr = JSON.stringify({
        'peer':username,
        'action':action,
        'message':message,
        'type':'send_sdp'
    })
    chatSocket.send(jsonStr)
}
function dcOnMessage(){}

