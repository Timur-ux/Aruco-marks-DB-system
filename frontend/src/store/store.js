import { configureStore } from "@reduxjs/toolkit";
import { loginReducer, passwordReducer } from "../reducer/authReducer";
import {tableReducer} from "../reducer/table"
import { requestsReducer } from "../reducer/requests";

export const store = configureStore({
  reducer: {
    login: loginReducer,
    password: passwordReducer,
    table: tableReducer,
    requests: requestsReducer,
  }
});
