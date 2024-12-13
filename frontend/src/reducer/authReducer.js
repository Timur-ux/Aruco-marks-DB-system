import { createTextFieldReducer } from "./textField";
import { createSlice } from "@reduxjs/toolkit";

const login = createTextFieldReducer("login")
const password = createTextFieldReducer("password")
const access = createSlice({
    name: "access",
    initialState: {
      value: "user"
    },
    reducers: {
      setAccess(state, action) {
        state.value = action.payload;
      }
    }
  });


export const setLogin = login.actions.setString;
export const setPassword = password.actions.setString;
export const setAccess = access.actions.setAccess;

export const loginReducer = login.reducer;
export const passwordReducer = password.reducer;
export const accessReducer = access.reducer;

