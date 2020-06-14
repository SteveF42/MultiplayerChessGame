var socket = io.connect('http://127.0.0.1:5000/')


socket.on('connect', function () {
    console.log('connected')
})


$('#findGame').on('click', function(){
    socket.emit('searching',function(callback){
        if(callback != undefined){
            window.location = callback
        }
    })
})

socket.on('disconnect-client', async function(gameID){
    const myGameID = await fetch('/getGameId')
    if(myGameId != null && myGameID == gameID){
        socket.emit('disconnect-other-client', gameID)
    }
})
