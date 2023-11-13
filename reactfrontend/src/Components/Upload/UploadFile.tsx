import http from "./http-common";
import axios from "../../axios";
import {BackendApi} from "../../backendApi";

const upload = (file: File, onUploadProgress: any, seperator : any, lines : any, timeMode : any): Promise<any> => {
    let body = {name : file.name,
                typeOfSchema : timeMode,
                delimiter : seperator,
                csv : lines
    };
    return BackendApi.uploadFile(body);
};

const getFiles = () : Promise<any> => {
    return http.get("/getFiles");
};
const download = (data :any) : Promise<any> => {
    return http.post('/download', data ,{responseType: 'blob'})
}
const FileUploadService = {
    upload,
    getFiles,
    download,
};
export default FileUploadService;
