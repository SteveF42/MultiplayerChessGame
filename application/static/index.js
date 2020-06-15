var socket = io.connect('http://127.0.0.1:5000/')


socket.on('connect', function () {
    console.log('connected')
})

socket.on('client-game-setup', async function(gameID){
    socket.emit('get-client-id')
    socket.on('response',id=>{
        let clientID = undefined
        let name = "None"
        if(id != undefined){
            clientID = id['gameID']
            name = id['name']
        }

        console.log(clientID,name)
    })

})


window.onload = function(){
    socket.emit('stop-processes',function(){
    })
}

$('#sendAnswer').on('click', function(){
    let answer = $('#sendAnswer').val()
    $('#sendAnswer').val('')
    socket.emit('move',answer)
})

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

