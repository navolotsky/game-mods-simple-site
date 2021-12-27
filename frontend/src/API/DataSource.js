import axios from "../utils/axios-config.js"

export default class DataSource {
    static async getMods(filters, limit = 10, offset = 0) {
        const {gameId = null, categoryId = null} = filters
        return await axios.get('api/mods/', {
            params: {
                game__id: gameId,
                category__id: categoryId,
                limit: limit,
                offset: offset
            }
        });
    }

    static async getGamesForSidebar(modsCategoryId = null) {
        return await axios.get(
            "api/games/get_list_for_menu/", {params: {mods_category_id: modsCategoryId}});
    }

    static async getModCategoriesForSidebar(gameId = null) {
        return await axios.get("api/categories/get_list_for_menu/", {params: {game_id: gameId}});
    }

    static async getMod(id, versionId) {
        return await axios.get(`api/mods/${id}`, {params: {version_id: versionId}});
    }
}
