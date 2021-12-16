import axios from "../utils/axios-config.js"

export default class DataSource {
    static async getMods(gameId, limit = 10, offset = 0) {
        console.log("айди игры = ", gameId)
        const response = await axios.get('api/mods/', {
            params: {
                game__id: gameId,
                limit: limit,
                offset: offset
            }
        })
        return response;
    }

    static async getGamesForSidebar() {
        const response = await axios.get("api/games/get_list_for_menu/")
        return response;
    }
}
