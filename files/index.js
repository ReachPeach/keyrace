async function createPlayer(name) {
    let request = await fetch('/api/v1/player/create', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded'
        },
        body: 'name=' + name

    })
    return await request.text()
}

async function createGame(playerId) {
    let text_length = Math.floor(Math.random() * 50) + 50;
    let request = await fetch('/api/v1/game/create', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded'
        },
        body: "text_length=" + text_length + "&players=" + playerId
    })
    return await request.text()
}

async function getGameInfo(gameId) {
    let request = await fetch('/api/v1/game/info?id=' + gameId, {
        method: 'GET',
    })
    return await request.json()
}

async function getGameStateInfo(gameId) {
    let request = await fetch('/api/v1/game/state/info?id=' + gameId, {
        method: 'GET',
    })
    return await request.json()
}

let gameId;

let gameStateInfo;

async function updateGameStateInfo(playerId) {
    gameStateInfo = await getGameStateInfo(gameId)
    document.getElementById('playerScore').innerText = gameStateInfo.score[playerId]
    if (gameStateInfo.winner) {
        document.getElementById('playerScore').style.color = 'blue'
        document.getElementById('playerScore').style.background = 'green'
    }
}

let playerId;

async function changeGameState(delta) {
    await fetch('/api/v1/game/state/change', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded'
        },
        body: "game_id=" + gameId + "&player_id=" + playerId + "&delta=" + delta
    });
}

async function startGame() {
    await fetch('/api/v1/game/start', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded'
        },
        body: "id=" + gameId
    });
}


let gameInfo;
let currentTextPosition = 0;
let text;

async function onKeyDownHandler(event) {
    if (event.key === text[currentTextPosition]) {
        ++currentTextPosition
        await changeGameState(1)
        await updateGameStateInfo(playerId)
    }
}

async function onLoad() {
    playerId = await createPlayer("p1")
    gameId = await createGame(playerId)
    gameInfo = await getGameInfo(gameId)
    document.getElementById('inputarea').innerText = gameInfo.text
    text = gameInfo.text
    await updateGameStateInfo(playerId)
    window.onkeydown = onKeyDownHandler
    await startGame()
}


