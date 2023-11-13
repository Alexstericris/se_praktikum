import axios from "axios";

export default axios.create({
    baseURL: "https://9070499e-4612-41d7-ab32-a3380b12a0db.mock.pstmn.io",
    headers: {
        "Content-type": "application/json",
    },
});
