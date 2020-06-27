var socket = io('http://127.0.0.1:5000/')
var private_socket = io('http://127.0.0.1:5000/private')

var clientID = undefined
var in_game = false

function HTML(msg,type) {
    let alert =
        `<p class="alert alert-${type} alert-dismissible", style="margin: 10px 25% 0 25%;", id="flashed-message",value="true">
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
socket.on('client-game-setup', async function (playerNames) {

    $('#flash-message').append(HTML('Game Found!','success'))
    let item = document.getElementById('hidden-message')
    item.style.display = "none"
    in_game = true

    $('#game-messages').append('Game Found! Say Hello!')

    $('#flashed-message').remove()
    $('#flashed-message').remove()
    $('#findGame').text('Find Game')

    let p1_name = playerNames[0]
    let p2_name = playerNames[1]
    document.getElementById('player1').innerHTML = p1_name
    document.getElementById('player2').innerHTML = p2_name
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
                $('#flash-message').append(HTML('Searching for game!'),'success')
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
    document.getElementById('player1_avatar').src = arr[num]

    num = Math.floor(Math.random() * arr.length)
    document.getElementById('player2_avatar').src = arr[num]
}


let current_choice = 0
let locked_in = false
$('#rock').on('click', function () {
    if(locked_in)
        return
        
    document.getElementById('rock').style.backgroundColor = 'rgb(71, 241, 65)'
    document.getElementById('paper').style.backgroundColor = 'rgb(0,0,0,0)'
    document.getElementById('scissors').style.backgroundColor = 'rgb(0,0,0,0)'
    current_choice = 1
})

$('#paper').on('click', function () {
    if(locked_in)
        return

    document.getElementById('rock').style.backgroundColor = 'rgb(0,0,0,0)'
    document.getElementById('paper').style.backgroundColor = 'rgb(71, 241, 65)'
    document.getElementById('scissors').style.backgroundColor = 'rgb(0,0,0,0)'
    current_choice = 2
})

$('#scissors').on('click', function () {
    if(locked_in)
        return

    document.getElementById('rock').style.backgroundColor = 'rgb(0,0,0,0)'
    document.getElementById('paper').style.backgroundColor = 'rgb(0,0,0,0)'
    document.getElementById('scissors').style.backgroundColor = 'rgb(71, 241, 65)'
    current_choice = 3
})

$('#lock-in-choice').on('click',function(){
    if(current_choice === 0){
        $('#flashed-message').remove()
        let s = HTML('select a choice','danger')
        $('#error').append(s)
        return
    }
    $('#flashed-message').remove()

    document.getElementById('lock-in-choice').setAttribute('disabled','disabled')
    document.getElementById('lock-in-choice').innerHTML = "WAITING FOR OPPONENT"
    locked_in=true
})
