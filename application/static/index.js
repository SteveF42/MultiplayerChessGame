var socket = io.connect('http://127.0.0.1:5000/')
var private_socket = io('http://127.0.0.1:5000/private')

var clientID = undefined
var in_game = false

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
    $('#flashed-message').remove()
    $('#flash-message').append(HTML('Game Found!'))
    let item = document.getElementById('hidden-message')
    item.style.display = "none"
    in_game = true
})

socket.on('received-message',msg=>{
    console.log(msg)
    let tag = `<p>${msg['name']}: ${msg['message']}</p>`
    $('#game-messages').append(tag)
})

window.onload = function(){
    socket.emit('stop-processes',function(){
    })
}

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
$('#send-friendly-message').on('click',function(){
    if(in_game===false){
        console.log('NOPE')
        return
    }

    let msg = $('#friendly-message').val()
    $('#friendly-message').val('')
    if(msg.length < 1 || msg == undefined){
        console.log("NOPE")
        return
    }
    console.log(msg)
    socket.emit('room-message',msg)
})

