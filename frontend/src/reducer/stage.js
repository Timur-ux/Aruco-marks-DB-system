import { createSlice } from "@reduxjs/toolkit";


export const stageReducer = createSlice({
    name: "stage",
    initialState: {
      value: "logging"
    },
    reducers: {
      login() {
        state.value = "login"
      },
      register() {
        state.value = "register"
      },
      requestsList() {
        state.value = "requestsList"
      }
    }
  });

