import { createSlice } from "@reduxjs/toolkit";


export const createTextFieldReducer = name =>
  createSlice({
    name: name,
    initialState: {
      value: ""
    },
    reducers: {
      setString(state, action) {
        state.value = action.payload;
      }
    }
  });
