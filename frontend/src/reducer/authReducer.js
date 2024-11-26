import { createTextFieldReducer } from "./textField";

const login = createTextFieldReducer("login")
const password = createTextFieldReducer("password")


export const setLogin = login.actions.setString;
export const setPassword = password.actions.setString;
export const loginReducer = login.reducer;
export const passwordReducer = password.reducer;

