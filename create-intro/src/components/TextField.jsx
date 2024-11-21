import React, { useState } from "react";

const TextField = ({label, blockStyle, fieldStyle}) => {
    const [text, setText] = useState("");
    const onTextChange = (e) =>
      setText(e.target.value);
    
    const onTextBlur = (e) =>
      console.log("text: ", text);

  return (
    <div style={blockStyle}>
      <p>{label}</p>
      <input style={fieldStyle} type="text" onChange={onTextChange} onBlur={onTextBlur}></input>
    </div>
  )
};

export default TextField;
