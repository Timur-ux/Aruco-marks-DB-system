import React from "react";
import style from "../style";
import ProfileData from "./ProfileData";


const UserPage = () => (
    <div style={style.mainBlock}>
      <ProfileData profileName="Пользователь" />
      <div style={{...style.mainForm, ...style.centered}}>
        <p><h3> Выберите действие: </h3></p>
      </div>
    </div>
);

export default UserPage;
