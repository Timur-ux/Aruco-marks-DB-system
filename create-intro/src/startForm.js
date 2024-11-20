import style from "./style.js";
import React from "react";
import { useNavigate } from "react-router-dom";

const StartForm = () => {
  const navigate = useNavigate();

  const onUserClick = (event) => {
    console.log("User clicked");
    navigate("/user");
  };

  const onAdminClick = (event) => {
    console.log("Admin clicked");
    navigate("/admin");
  };

  return (
    <div
      style={{
        ...style.centeredWidth,
        ...style.textCentered,
        ...style.mainForm,
      }}
    >
      <p>
        Добро пожаловать в сервис отслеживания Aruco меток <br />
        Выберите профиль:
      </p>
      <div style={style.justifiedContent}>
        <button style={style.mainForm} onClick={onUserClick}>Пользователь</button>
        <button style={style.mainForm} onClick={onAdminClick}>Администратор</button>
      </div>
    </div>
  );
}

export default StartForm;
