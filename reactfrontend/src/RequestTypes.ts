export type loginUserRequest = {
    username: string,
    password: string
}
export type roles={
    is_admin:Boolean,
    is_data_analyst:Boolean,
    is_simulation_engineer:Boolean,
    is_data_owner:Boolean,
}

export type loginUserResponse = { // Set-Cookie: token=string
    roles:string[]
}

export type logEntry = {
    userName: string,
    timestamp: string,
    action: string,
}

export type getLogRequest = {
    from?: string, //timestamp
    to?: string, //timestamp
    userNames: string[]
}

export type getLogResponse = {
    entries: logEntry[]
}

export type columnEntry = {
    timestamp: number, //ms since start
    value?: number
}

export type columnInfo = {
    id: number,
    name: string,
}

export type column = {
    data: columnEntry[],
    unit: string,
}


export type filterApplyRequest = {
    databaseIdInput: string,
    filter: number[], //1-8
    parameter: number[][], // same order as filters
    from: number,
    to: number
}

export type filterApplySaveRequest = {
    databaseIdInput: string,
    databaseIdOutput: string,
    filter: number[], //1-8
    parameter: number[][], // same order as filters
    from: number,
    to: number
}

export type filterApplyResponse = {
    data: column,
}

export type FileMetadata = {
    id: number
    name: string,
    timeRecorded: string,
    creator: string,
    baseId?: number,
    columns: columnInfo[]
}

export type getMyFilenamesResponse = UserFiles

export type UserFiles = {
    username: string
    filenames: FileMetadata[]
}

export type getAllFilenamesResponse = {
    userdata: UserFiles[],
}



export type isFilenameAvailableResponse = {
    available: boolean,
}

export enum schema{
    dictionaryOfKeys,
    matrix
}

export type fileUploadRequest = {
    name: string,
    schema: string
}

export type deleteFileRequest = {
    databaseId: string
}

