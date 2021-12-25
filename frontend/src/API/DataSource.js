import axios from "../utils/axios-config.js"

export default class DataSource {
    static async getMods(filters, limit = 10, offset = 0) {
        const {gameId = null, categoryId = null} = filters
        const response = await axios.get('api/mods/', {
            params: {
                game__id: gameId,
                category__id: categoryId,
                limit: limit,
                offset: offset
            }
        })
        return response;
    }

    static async getGamesForSidebar(modsCategoryId = null) {
        const response = await axios.get(
            "api/games/get_list_for_menu/", {params: {mods_category_id: modsCategoryId}})
        return response;
    }

    static async getModCategoriesForSidebar(gameId = null) {
        const response = await axios.get("api/categories/get_list_for_menu/", {params: {game_id: gameId}})
        return response;
    }
}
