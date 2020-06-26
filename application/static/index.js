var socket = io('http://127.0.0.1:5000/')
var private_socket = io('http://127.0.0.1:5000/private')

var clientID = undefined
var in_game = false

function HTML(msg) {
    let alert =
        `<p class="alert alert-success alert-dismissible", style="margin: 10px 25% 0 25%;", id="flashed-message",value="true">
        ${msg}
        <button type="button" class="close" data-dismiss="alert" aria-label="Close">
        <span aria-hidden="true">&times;</span>
        </button>
        </p>`
    return alert
}
//socket events
socket.on('connect', function () {
    console.log('connected')

})

//after the other client disconnects, resets the server info and client info
socket.on('force-end-game', function (name) {
    console.log('other client disconnected')
    in_game = false

    let tag = `<li style="margin-top:0; list-style: none" id="client-message">${name} has disconected... </li>`
    $('#game-messages').append(tag)

    socket.emit('pop-gamekey')
    let item = document.getElementById('hidden-message')
    item.style.display = "flex"

})
//sets up client to play game
socket.on('client-game-setup', async function (sessionInfo) {
    console.log(sessionInfo)
    $('#flash-message').append(HTML('Game Found!'))
    let item = document.getElementById('hidden-message')
    item.style.display = "none"
    in_game = true

    $('#game-messages').append('Game Found! Say Hello!')

    
    $('#flashed-message').remove()
    $('#flashed-message').remove()
    $('#findGame').text('Find Game')
})
//chat window 
socket.on('received-message', msg => {
    let tag = `<li style="margin-top:0; list-style: none" id="client-message">${msg['name']}: ${msg['message']}</li>`
    $('#game-messages').append(tag)
})


// window.onload = function(){
//     socket.emit('stop-processes',function(){
//     })
// }


//HTML events
//searches for game
$('#findGame').on('click', function () {
    socket.emit('searching', function (url, boolValue) {
        if (url != undefined)
            window.location = url
        else {
            if (boolValue) {
                $('#findGame').text('Stop Searching')
                $('#flash-message').append(HTML('Searching for game!'))
                searching = false
            } else {
                $('#flashed-message').remove()
                $('#findGame').text('Find Game')
                searching = true
            }
        }
    })
})
//send message event
$('#send-friendly-message').on('click', function () {
    if (in_game === false) {
        console.log('NOPE')
        return
    }

    let msg = $('#friendly-message').val()
    $('#friendly-message').val('')
    if (msg.length < 1 || msg == undefined) {
        console.log("NOPE")
        return
    }
    socket.emit('room-message', msg)
})

window.onload = async function () {
    arr = [
        '/static/images/player-icon1.png',
        '/static/images/player-icon2.png',
        '/static/images/player-icon3.png',
    ]

    let num = Math.floor(Math.random() * arr.length)
    console.log(num)
    document.getElementById('player1_avatar').src=arr[num]

    num = Math.floor(Math.random() * arr.length)
    document.getElementById('player2_avatar').src=arr[num]
}

$('#rock').on('click',()=>{

})

$('#paper').on('click',()=>{

})

$('#scissors').on('click',()=>{
    
})
