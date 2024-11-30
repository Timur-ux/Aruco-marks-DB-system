import React from "react";
import style from "../style";
import TableRow from "./TableRow";

const Table = ({columns, rows}) => {
  console.log("Table: arg: columns: ", columns)
  console.log("Table: arg: rows: ", rows)

  const header = <TableRow row={columns}/>
  const tableRows = rows.map(data => <TableRow row={data} />);

  console.log("Table: value: header: ", header)
  console.log("Table: value: rows: ", tableRows)

  return (
    <table style={{...style.mainForm, ...style.centered, ...style.table}}>
      {header}
      {tableRows}
    </table>
  );
}


export default Table;
