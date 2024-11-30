import { createSlice } from "@reduxjs/toolkit";


const tableReducer_ = createSlice({
  name: "table-data",
  initialState: {
    columns: [],
    rows: []
  },
  reducers: {
    setColumns(state, action) {
      state.columns = action.payload
    },
    setRows(state, action) {
      state.rows = action.payload
    }
  }
});


export const selectColumns = (state) => state.table.columns;
export const selectRows = (state) => state.table.rows;

export const {setColumns, setRows} = tableReducer_.actions;
export const tableReducer = tableReducer_.reducer;
