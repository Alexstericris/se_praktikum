import {getAllFilenamesResponse, getMyFilenamesResponse} from "../RequestTypes";
import axios from "../axios";
import {BackendApi} from "../backendApi";

// const treeMockdata: getAllFilenamesResponse = {
    // userdata: [
    //     {
    //         username: "user1",
    //         filenames: [
    //             {id: 5, name: "file1", timeRecorded: "idc", creator: "dieter", baseId: 69, columnInfos: [
    //                     {
    //                         id: 1,
    //                         name: "col1",
    //                     },
    //                     {
    //                         id: 2,
    //                         name: "col2",
    //                     }
    //                 ]},
    //             {id: 6, name: "file2", timeRecorded: "idc", creator: "dieter", baseId: 69, columnInfos: [
    //                     {
    //                         id: 3,
    //                         name: "col1",
    //                     },
    //                     {
    //                         id: 4,
    //                         name: "col2",
    //                     }
    //                 ]}
    //         ]
    //     }
    // ]

// }

export function getMyFilenames(callback: (val : getMyFilenamesResponse) => void){
    axios.get("/getMyFilenames/").then((val) => {
        callback(val.data as getMyFilenamesResponse)
    })
}
export function getAllFilenames(callback: (val : getAllFilenamesResponse) => void){
    BackendApi.getAllUserFilenames().then((val) => {

        callback(val.data as getAllFilenamesResponse)
    })
}