import React from "react";
import { useSelector } from "react-redux";
import style from "../style";
import Table from "./Table";


const TableGenerator = () => {
  console.log("TableGenerator invoked");
  const columns = useSelector(state => state.table.columns)
  const rows = useSelector(state => state.table.rows)

  return (
    <div>
      <Table style={{...style.mainForm, ...style.table}}columns={columns} rows={rows}/>
    </div>
);
}


export default TableGenerator;
