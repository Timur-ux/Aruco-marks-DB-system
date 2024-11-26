import { configureStore } from "@reduxjs/toolkit";
import { loginReducer, passwordReducer } from "../reducer/authReducer";

export const store = configureStore({
  reducer: {
    login: loginReducer,
    password: passwordReducer
  }
});
