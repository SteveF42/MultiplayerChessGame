var socket = io.connect('http://127.0.0.1:5000/')
var private_socket = io('http://127.0.0.1:5000/private')
var clientID = undefined
var searching = true

function HTML(msg){
    let alert = 
        `<p class="alert alert-success alert-dismissible ", style="margin: 10px 25% 0 25%;", id="flashed-message",value="true">
        ${msg}
        <button type="button" class="close" data-dismiss="alert" aria-label="Close">
        <span aria-hidden="true">&times;</span>
        </button>
        </p>`
        return alert
}

socket.on('connect', function () {
    console.log('connected')
})

socket.on('client-game-setup', async function(sessionInfo){
    console.log(sessionInfo)
    let val = $('#flashed-message').val()

    $('#flashed-message').remove()
    
    $('#flash-message').append(HTML('Game Found!'))
    
})

window.onload = function(){
    socket.emit('stop-processes',function(){
    })
}

$('#sendAnswer').on('click', function(){
    let move = $('#inputAnswer').val()
    $('#inputAnswer').val('')
    socket.emit('game-info',move,callback=>{
        console.log(callback)
    })
})

$('#findGame').on('click', function(){
    socket.emit('searching',function(url,boolValue){
        if(url!=undefined)
            window.location = url
        else{
            if(boolValue){
                $('#findGame').text('Stop Searching')
                $('#flash-message').append(HTML('Searching for game!'))
                searching=false
            }else{
                $('#flashed-message').remove()
                $('#findGame').text('Find Game')
                searching=true
            }
        }
    })

})

