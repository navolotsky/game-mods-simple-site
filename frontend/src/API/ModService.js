import axios from "../utils/axios-config.js"

export default class ModService {

    static async getAll(limit = 10, offset = 0) {
        const response = await axios.get('api/mods/', {
            params: {
                limit: limit,
                offset: offset
            }
        })
        return response;
    }
}
