var socket = io.connect('http://127.0.0.1:5000/')


socket.on('connect', function () {
    console.log('connected')
})

socket.on('disconnect-client', function(gameID, clientGameID){
    console.log(gameID,clientGameID)
    if(gameID == clientGameID){
        socket.emit('disconnect-other-client', gameID)
    }
})
socket.on('client-game-setup',function(gameID,clientID){
    console.log(gameID,clientID)
    if(gameID === clientID){
        socket.emit('start-game',gameID)
    }
})
socket.on('disconnect',()=>{
    socket.emit('disconnect-server-side')
})


window.onload = function(){
    socket.emit('stop-processes',function(){

    })
}



$('#sendAnswer').on('click', function(){
    let move = $('#inputAnswer').val()
    $('#inputAnswer').val('')
    socket.emit('move',move)
})


$('#findGame').on('click', function(){
    socket.emit('searching',function(callback){
        if(callback != undefined){
            window.location = callback
        }
    })
})

