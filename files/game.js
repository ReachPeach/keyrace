let gameId;
let playerId;
let gameStateInfo

async function getGameInfo() {
    let request = await fetch('/api/v1/game/info?id=' + gameId, {
        method: 'GET',
    })
    return await request.json()
}

async function getGameStateInfo() {
    let request = await fetch('/api/v1/game/state/info?id=' + gameId, {
        method: 'GET',
    })
    return await request.json()
}

async function changeGameState(delta) {
    await fetch('/api/v1/game/state/change', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded'
        },
        body: "game_id=" + gameId + "&player_id=" + playerId + "&delta=" + delta
    });
}

async function updateGameStateInfo() {
    gameStateInfo = await getGameStateInfo()
    if (gameStateInfo.winner) {
        // TODO:
        // document.getElementById('userProgress').style.color = 'blue'
        // document.getElementById('userProgress').style.background = 'green'
    } else {
        for (const [i, value] of players_ids.entries()) {
            let progressBar = document.getElementsByClassName("progressBar")[i]
            let userScore = document.getElementsByClassName("score")[i]
            progressBar.value = gameStateInfo.score[value] / generated_text.length
            userScore.innerText = Math.round((gameStateInfo.score[value] / generated_text.length + Number.EPSILON) * 100).toString() + "%"
        }
    }
}

async function onKeyDownHandler(event) {
    let remainingText = document.getElementById("remainingText")
    if (event.key === remainingText.innerText[0]) {
        let correctText = document.getElementById("correctText")
        remainingText.innerText = remainingText.innerText.substring(1)
        correctText.innerText += event.key
        await changeGameState(1)
        await updateGameStateInfo()
    }
}

async function startGame() {
    await fetch('/api/v1/game/start', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded'
        },
        body: "game_id=" + gameId + "&player_id=" + playerId
    });
}

let gameSocket
let gameStateSocket

async function onReadyClick() {
    document.getElementById('playerReady').style.visibility = "hidden"
    let ready_count = document.getElementById("ready")
    ready_count.innerText = (Number(ready_count.innerText) + 1).toString()
    await startGame()
}

async function getGameId() {
    let request = await fetch('/api/v1/session/get/game_id', {
        method: 'GET',
    })
    return await request.text()
}

async function getPlayerId() {
    let request = await fetch('/api/v1/session/get/player_id', {
        method: 'GET',
    })
    return await request.text()
}

function onGameStart(gameStateInfo) {
    let helpElement = document.getElementById("help")
    helpElement.style.visibility = "collapsed"
    helpElement.innerText = ""

    let correctText = document.getElementById("correctText")
    correctText.style.visibility = "visible"
    correctText.innerText = ""

    let remainingText = document.getElementById("remainingText")
    remainingText.style.visibility = "visible"
    remainingText.innerText = generated_text

    let progressBars = document.getElementById("usersProgress")
    progressBars.style.visibility = "visible"

    for (let player_id of players_ids) {
        let userProgressT = document.querySelector("#userProgressT").content.cloneNode(true)
        let userName = userProgressT.querySelector("#name")
        userName.textContent += player_id
        progressBars.appendChild(userProgressT)
    }

    window.onkeydown = onKeyDownHandler
}

function onGameChanged() {

}

let generated_text
let players_ids

function updateGameParameters(gameInfo) {
    generated_text = gameInfo.text
    players_ids = gameInfo.players.split(',')
    document.getElementById('all').innerText = players_ids.length
}

function onGameHandler(event) {
    let game = JSON.parse(event.data)
    updateGameParameters(game)
}

function onGameFinish() {
    // TODO
    console.log("Game finished!")
}

function onGameStateHandler(event) {
    let gameState = JSON.parse(event.data)
    console.log(gameState.score)
    players_ids = Object.keys(gameState.score)
    console.log(players_ids)

    if (gameState.type === "IN_PROGRESS") {
        onGameStart(gameState)
    }
    if (gameState.type === "DONE") {
        onGameFinish()
    }
}

async function sendWhenReady(socket, message) {
    while (socket.readyState === 0) {
        await new Promise(r => setTimeout(r, 400));
    }
    if (socket.readyState === 1) {
        socket.send(message)
    }
}

async function onLoad() {
    gameId = await getGameId()
    playerId = await getPlayerId()
    await updateGameParameters(await getGameInfo())

    gameSocket = new WebSocket('ws://' + location.host + '/api/v1/m/game?game_id=' + gameId);
    gameSocket.onmessage = onGameHandler

    gameStateSocket = new WebSocket('ws://' + location.host + '/api/v1/m/game/state?game_id=' + gameId)
    gameStateSocket.onmessage = onGameStateHandler
}