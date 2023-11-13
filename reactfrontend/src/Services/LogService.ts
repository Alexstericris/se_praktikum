import { logEntry} from "../RequestTypes";

export const LogMockdata: logEntry[] = [{
    "userName": "dataOwner",
    "timestamp": "2023-01-22-11-23-23",
    "action": "upload"
},
    {
        "userName": "simulationsEngineer",
        "timestamp": "2023-04-22-11-23-23",
        "action": "filtered graph3"
    },
    {
        "userName": "admin",
        "timestamp": "2023-08-22-11-23-23",
        "action": "checked Log"
    },
    {
        "userName": "dataAnalyst",
        "timestamp": "2023-05-22-11-23-23",
        "action": "analysed"
    },
    {
        "userName": "dataOwner",
        "timestamp": "2023-07-22-11-23-23",
        "action": "LogIn"
    },
    {
        "userName": "Admin",
        "timestamp": "2023-06-22-11-23-23",
        "action": "LogIn"
    },
    {
        "userName": "systemsEngineer",
        "timestamp": "2023-03-22-11-23-23",
        "action": "update graph"
    },
    {
        "userName": "dataOwner",
        "timestamp": "2023-02-22-11-23-23",
        "action": "uploaded file"
    }]

export const LogMockdata2: logEntry[] = [{
    "userName": "dataOwner",
    "timestamp": "2023-01-22-11-23-23",
    "action": "upload"
},
    {
        "userName": "simulationsEngineer",
        "timestamp": "2023-04-22-11-23-23",
        "action": "filtered graph3"
    }
]

export function mapMonth(month: string) {
    switch (month) {
        case "Jan":
            return "01";
        case "Feb":
            return "02";
        case "Mar":
            return "03";
        case "Apr":
            return "04";
        case "May":
            return "05";
        case "Jun":
            return "06";
        case "Jul":
            return "07";
        case "Aug":
            return "08";
        case "Sep":
            return "09";
        case "Oct":
            return "10";
        case "Nov":
            return "11";
        case "Dec":
            return "12";

    }
}

export function formatDate(event:any){
    let year = event.$d.toString().slice(11, 16)
    let day = event.$d.toString().slice(7, 10)
    let month = mapMonth(event.$d.toString().slice(4,7))
    let calendar = (year + month + day).replaceAll(" ", "-")
    let time = event.$d.toString().slice(16, 24)
    return (calendar + " " +time)
}
