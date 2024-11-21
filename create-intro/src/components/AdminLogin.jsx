import React, { useState } from "react";
import style from "../style";
import ProfileData from "./ProfileData";
import TextField from "./TextField";

const AdminLogin = () => {
  const onSendClick = () => {
    console.log("clicked");
  }

  return (
  <div style={style.mainBlock}>
    <ProfileData profileName="Администратор"/>

    <div style={{...style.centered, ...style.mainForm}}>
      <h3 style={style.centeredWidth}>Авторизация</h3>
      <TextField label="Login" fieldStyle={style.logInDataField}/>
      <TextField label="Password" type="password" fieldStyle={style.logInDataField} />
      <div style = {{...style.justifiedContent, ...style.centeredWidth}}>
          <button style={style.mainForm} onClick={onSendClick}>Отправить</button>
      </div>
    </div>
  </div>
  )
};

export default AdminLogin;
