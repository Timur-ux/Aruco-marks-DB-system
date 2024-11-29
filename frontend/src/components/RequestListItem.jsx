import React from "react";
import style from "../style";

const RequestListItem = ({label, uri}) => {
  const onClick = () =>
    console.log("URI: ", uri)

  return (
    <button style={style.button} onClick={onClick}>{label}</button>
  )
}

export default RequestListItem;
