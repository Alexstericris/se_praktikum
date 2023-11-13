import {createContext, useReducer} from "react";
import {User} from "./types";
export const UserContext = createContext(null);
export const UserDispatchContext = createContext((val:any)=>{return val});

export function userReducer(user:any, newUser:User|null){
        user = newUser;
    return user;
}

export function UserContextProvider(props:any) {
    const [user, dispatch] = useReducer(userReducer, null);
    return (
        <UserContext.Provider value={user}>
            <UserDispatchContext.Provider value={dispatch}>
                {props.children}
            </UserDispatchContext.Provider>
        </UserContext.Provider>
    );
}