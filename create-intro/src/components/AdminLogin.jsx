import React, { useState, useEffect } from "react";
import style from "../style";
import ProfileData from "./ProfileData";
import TextField from "./TextField";
import axios from "axios";
import addresses from "../addresses";

const client = axios.create({
  baseURL: addresses.backend
});

const AdminLogin = () => {
  const onSendClick = () => {
    console.log('clicked');
    const uri = '/api/login';
    (
      async () => {
      await client({method: "GET", url: uri})
        .then((response) => {console.log(response.data)})
        .catch((error) => {console.log(error)});
      }
    )()
    console.log('clicked2');
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
