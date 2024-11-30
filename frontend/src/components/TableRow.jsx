import React from "react";
import style from "../style";
import TableCell from "./TableCell";
import cellDataToStr from "../service/cellDataToStr";


const TableRow = ({row}) => {
  console.log("Table row: args: row: ", row);

  const values = []
  Object.keys(row).forEach((key, _) => values.push(cellDataToStr(row[key])));

  return (<tr style={style.tableRow}>{values.map(value => <TableCell value={value}/>)}</tr>);

}

export default TableRow;
