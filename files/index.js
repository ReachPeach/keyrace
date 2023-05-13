async function putData(key_name, key_value) {
    await fetch('/api/v1/session/put', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded'
        },
        body: 'key_name=' + key_name + '&key_value=' + key_value
    })
}

async function createPlayer(name) {
    let request = await fetch('/api/v1/player/create', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded'
        },
        body: 'name=' + name

    })

    playerId = await request.text()
    await putData('player_id', playerId)
    return playerId
}

async function forwardToGame(gameId) {
    await putData('game_id', gameId)
    window.location.href = "/api/v1/file/game.html"
}

async function createNewGame() {
    let text_length = Math.floor(Math.random() * 50) + 50;
    let request = await fetch('/api/v1/game/create', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded'
        },
        body: "text_length=" + text_length + "&players=" + playerId
    })

    let gameId = await request.text()
    await forwardToGame(gameId)
}

let playerId

function forwardToGameHandler(gameId) {
    return async () => {
        console.log(gameId, playerId)
        let request = await fetch('/api/v1/game/join', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/x-www-form-urlencoded'
            },
            body: "game_id=" + gameId + "&player_id=" + playerId
        })

        await request
        await forwardToGame(gameId)
    }
}

async function fillOpenedGames() {
    let request = await fetch('/api/v1/games/ids', {
        method: 'GET',
    })
    let gamesIds = await request.json()
    let gamesList = document.getElementById('openedGames')

    for (let gameId of gamesIds.ids) { // {ids, []}
        console.log(gameId)
        let gameElemClone = document.querySelector("#openedGame").content.cloneNode(true)
        let gameEnterLink = gameElemClone.querySelector("#game")
        gameEnterLink.textContent = gameId
        gameEnterLink.onclick = forwardToGameHandler(gameId)
        gameEnterLink.style.visibility = "visible"
        gamesList.appendChild(gameEnterLink)
    }
}

async function onLoad() {
    playerId = await createPlayer("p1")
    await fillOpenedGames()
}


