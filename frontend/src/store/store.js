import { applyMiddleware, configureStore } from "@reduxjs/toolkit";
import {
  loginReducer,
  passwordReducer,
  accessReducer,
} from "../reducer/authReducer";
import { tableReducer } from "../reducer/table";
import { requestsReducer } from "../reducer/requests";
import { thunk } from "redux-thunk";
import { profileReducer } from "../reducer/profile";

export const store = configureStore({
  reducer: {
    login: loginReducer,
    password: passwordReducer,
    access: accessReducer,
    table: tableReducer,
    requests: requestsReducer,
    profile: profileReducer,
  },
}, applyMiddleware(thunk));
