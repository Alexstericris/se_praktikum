import axios from "./axios";

export class BackendApi{

    static login(loginParameters:{username:string,password:string}) {
        return axios.post('/api/auth/login/', loginParameters, {
            headers: {
                Authorization: 'Bearer '+localStorage.getItem('access')
            }
        })
    }

    static register(registerParameters:{username:string,email:string,password:string}) {
        return axios.post('/api/auth/register/',registerParameters,{
            headers: {
                Authorization: 'Bearer '+localStorage.getItem('access')
            }
        })
    }

    static refresh() {
        return axios.post('/api/auth/refresh/',{
            refresh:localStorage.getItem('refreshToken')
        },{
            headers: {
                Authorization: 'Bearer '+localStorage.getItem('access')
            }
        })
    }

    static getMetadataColumn() {
        return axios.get('/api/metadata')
    }

    static filterApply(id:number|null=null,columnName:string='') {
        return axios.post('/api/filterApply/',{
            databaseColumnIdInput: id,
            filter:[],
            parameter:[]
        }, {
            headers: {
                Authorization: 'Bearer ' + localStorage.getItem('access')
            }
        })
    }

    static logs() {
        return axios.get('/api/logs',{
            headers: {
                Authorization: 'Bearer '+localStorage.getItem('access')
            }
        })
    }

    static getUser() {
        return axios.get('/getMyUserInformation/',{
            headers: {
                Authorization: 'Bearer '+localStorage.getItem('access')
            }
        })
    }
    static uploadFile(body:any) {
        return axios.post("/api/uploadFile/", body, {
            headers: {Authorization: 'Bearer ' + localStorage.getItem('access')}
        });

    }
    static getAllUserFilenames() {
        return axios.get("/api/getAllUserFilenames/", {
            headers: {Authorization: 'Bearer ' + localStorage.getItem('access')}
        });
    }
}