import React, { useEffect, useState } from "react";
import { useSelector } from "react-redux";
import { onFilled, setRows } from "../reducer/table";
import style from "../style";
import Table from "./Table";


const TableGenerator = () => {
  const state = useSelector(state => state)
  const columns = useSelector(state => state.table.columns)
  const rows = useSelector(state => state.table.rows)

  console.log("Table generator rendered");
  return (
    <div>
      <Table style={{...style.mainForm, ...style.table}}columns={columns} rows={rows}/>
    </div>
);
}


export default TableGenerator;
