import React from "react";
import style from "../style";

class DataField extends React.Component {

  onChange = (e) => this.props.states[this.props.idx] = e.target.value;

  render() {
    return (
      <input style={style.dataField} onChange={this.onChange} placeholder ={this.props.placeholder}/>
    )
  }
}
    
export default DataField;
