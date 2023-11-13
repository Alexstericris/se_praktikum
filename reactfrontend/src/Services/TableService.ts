import {filterApplyResponse, column, columnInfo} from "../RequestTypes";

export const mockTable: filterApplyResponse[] =
    [
        {data:{data:[{timestamp:1,value:4},{timestamp:2,value:8}],unit:"m/s"}},
        {data:{data:[{timestamp:1,value:3},{timestamp:2,value:99}],unit:"m"}}
    ]

export function getColumns(columns: columnInfo[], callback: (val : column[]) => void){
    callback(mockTable.map((far) => far.data))
}