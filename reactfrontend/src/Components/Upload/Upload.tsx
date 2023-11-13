import React, { useState } from 'react';
import Button from '@mui/material/Button';
import IconButton from '@mui/material/IconButton';
import {InputLabel} from "@mui/material";
import {NativeSelect,FormControl} from "@mui/material";
import ChangeEvent from '@mui/material/Select';
import "./Upload.css"
import UploadService from "./UploadFile";
import UploadFileSharpIcon from '@mui/icons-material/UploadFileSharp';
import SimCardDownloadSharpIcon from '@mui/icons-material/SimCardDownloadSharp';


export default function Upload(props: { setLoading: (loading: boolean) => void }) {

    const [currentFile, setCurrentFile] = useState<File>();
    //const [progress, setProgress] = useState<number>(0);
    //const [message, setMessage] = useState<string>("");
    //const [fileInfos, setFileInfos] = useState<Array<IFile>>([]);
    const [seperator, setSeperator] = useState(",");
    const [timeMode, setTimeMode] = useState("time_first_single")
    const [rows, setRows] = useState("");


    const selectFile = (event: React.ChangeEvent<HTMLInputElement>) => {
        const { files } = event.target;
        const selectedFiles = files as FileList;
        const file = selectedFiles.item(0);
        if (file == null) {
            return;
        }
        setCurrentFile(file)
        const reader = new FileReader();
        reader.onload = (e) => {
            if (e.target == null || typeof e.target.result !== "string") {
                return;
            }

            // Split the file contents into lines
            // const lines = e.target.result.split("\n");
            //const csv = lines.flatMap((line) => {
            //    let row = line.split(seperator)
            //    row.push("\n")
            //    return row}).join(seperator)
            const result = e.target.result.replace(",\n,","\n")
            setRows(result)
            return result
        };
        reader.readAsText(file);
    };
    const upload = () => {
        //setProgress(0);
        if (!currentFile) return;
        props.setLoading(true)
        UploadService.upload(currentFile, (event: any) => {
            //setProgress(Math.round((100 * event.loaded) / event.total));
        },seperator,rows,timeMode)
            .then((response) => {
                setCurrentFile(undefined)});
                //console.log(response.data)
                //setMessage(response.data.message);
                //return UploadService.getFiles();
           // })
            //.then((files) => {
               // console.log(files)
                //setFileInfos(files.data);
            //})
           // .catch((err) => {
                //setProgress(0);

                //if (err.response && err.response.data && err.response.data.message && err.message) {
                    //setMessage(err.message);
                //} else {
                    //setMessage("Could not upload the File!");
                //}

            /*    setCurrentFile(undefined);
            })
            .finally(() => props.setLoading(false))
             */
    };
    // @ts-ignore
    const handleSeperatorChange = (event : ChangeEvent<HTMLSelectElement>) => setSeperator(event.target.value);
    // @ts-ignore
    const handleTimeChange = (event : ChangeEvent<HTMLSelectElement>) => setTimeMode(event.target.value);
    const onDownload = () => {
        //const link = document.createElement("a");
        //link.download = `download.txt`;
        //link.href = "./download.txt";
        //link.click();
    };
    // @ts-ignore
    return (
        <div className= "interactionwidget">
            <div className={"buttonflex"}>
                <div className={"buttons"}>
                    <FormControl className={"select"} >
                        <InputLabel className = {"button"} style={{ color: '#fff' }} >Seperator </InputLabel>
                        <NativeSelect defaultValue={seperator}
                                      onChange={handleSeperatorChange} value = {seperator} style={{ color: '#fff' }} >
                            <option style={{ color: "#2B2B2B" }} value={";"}>SemiColon</option>
                            <option style={{ color: "#2B2B2B" }} value={","}>Comma</option>
                        </NativeSelect>
                    </FormControl>
                </div>
                <div className={"buttons"}>
                    <FormControl>
                        <InputLabel className = {"button"} style={{ color: '#fff' }} >Schema</InputLabel>
                        <NativeSelect defaultValue={timeMode} variant = {"filled"} onChange={handleTimeChange} className={"schemaButton"} style={{ color: '#fff' }} >
                            <option  style={{ color: "#2B2B2B" }} value={"time_first_single"} >time first single</option>
                            <option style={{ color: "#2B2B2B" }} value={"time_alternating"} >time alternating</option>
                        </NativeSelect>
                    </FormControl>
                </div>
                <div className={"buttons"}>
                    <Button className={"button"} variant={"contained"} component={"label"} style={{ color: '#fff' }} >
                        Select File
                        <label>
                            <input hidden = {!currentFile} accept={".csv"} type={"file"} onChange={selectFile}/>
                        </label>
                    </Button>
                </div>
            </div>
            <div className={"iconFlex"}>
                <div className={"iconDownload"}>
                    <IconButton>
                        <SimCardDownloadSharpIcon fontSize={"large"} style={{ color: '#fff' }}></SimCardDownloadSharpIcon>
                    </IconButton>
                </div>
                <div className={"iconUpload"}>
                    <IconButton disabled={!currentFile}>
                        <UploadFileSharpIcon onClick={upload} fontSize={"large"} style={{ color: '#fff' }}></UploadFileSharpIcon>
                    </IconButton>
                </div>
            </div>
        </div>
        // <div className= "interactionwidget">
        //     <div className = {"innerbox"}>
        //     <FormControl className={"select"} >
        //         <InputLabel className = {"input"} style={{ color: '#fff' }} >Numbers</InputLabel>
        //         <Select variant = {"filled"} onChange={handleChange} value = {value} label = {"Age"} className = {"form"} style={{ color: '#fff' }} >
        //             <MenuItem value={10}>Ten</MenuItem>
        //             <MenuItem value={20}>Twenty</MenuItem>
        //             <MenuItem value={30}>Thirty</MenuItem>
        //             <MenuItem value={40}>Fourty</MenuItem>
        //         </Select>
        //     </FormControl>
        //     <br/>
        //         <Button variant={"text"} component={"label"} size={"large"} style={{ color: '#fff' }} >
        //             Select File
        //             <label>
        //             <input hidden = {!currentFile} accept={".pdf"} type={"file"} onChange={selectFile}/>
        //             </label>
        //         </Button>
        //         <div className="col-4">
        //             <Button
        //                 className="uploadButton"
        //                 disabled={!currentFile}
        //                 onClick={upload}
        //             >
        //                 Upload
        //             </Button>
        //         </div>
        //         {currentFile && (
        //             <div className="progress my-3">
        //                 <div
        //                     className="progress-bar progress-bar-info"
        //                     role="progressbar"
        //                     aria-valuenow={progress}
        //                     aria-valuemin={0}
        //                     aria-valuemax={100}
        //                     style={{ width: progress + "%" }}
        //                 >
        //                     {progress}%
        //                 </div>
        //             </div>
        //         )}
        //         {message && (
        //             <div className="alert alert-secondary mt-3" role="alert">
        //                 {message}
        //             </div>
        //         )}
        //
        //         <div className="card mt-3">
        //             <div className="card-header">List of Files</div>
        //             <ul className="list-group list-group-flush">
        //                 {fileInfos &&
        //                     fileInfos.map((file, index) => (
        //                         <li className="list-group-item" key={index}>
        //                             <a href={file.url}>{file.name}</a>
        //                         </li>
        //                     ))}
        //             </ul>
        //         </div>
        //         <IconButton aria-label={"upload picture"} component={"label"} style={{ color: '#fff' }} >
        //             <input hidden accept={"image/*"} type={"file"} />
        //             <PhotoCamera/>
        //         </IconButton>
        //         <Button onClick={onDownload} variant={"text"} color={"secondary"} size={"large"} style={{ color: '#fff' }} >
        //             Download
        //         </Button>
        //     <br/>
        //     </div>
        // </div>

    );
}
