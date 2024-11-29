import { createSlice } from "@reduxjs/toolkit";

const requestsReducer_ = createSlice({
  name: "possible-requests",
  initialState: {
    requests: [],
  },
  reducers: {
    setRequests(state, action) {
      console.log("Setting requests: ", action.payload.requests);
      state.requests = action.payload.requests;
    },
    addRequests(state, action) {
      console.log("Adding requests: ", action.payload.requests);
      state.requests += action.payload.requests;
    },
  },
});

export const { setRequests, addRequests } = requestsReducer_.actions;
export const requestsReducer = requestsReducer_.reducer;
