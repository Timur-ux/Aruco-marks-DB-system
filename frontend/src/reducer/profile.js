import { createSlice } from "@reduxjs/toolkit";

const profileReducer_ = createSlice({
  name: "profile",
  initialState: {
    name: "Not set"
  },
  reducers: {
    setName(state, action) {
      state.name = action.payload;
    }
  }
});

export const {setName} = profileReducer_.actions;
export const profileReducer = profileReducer_.reducer;
