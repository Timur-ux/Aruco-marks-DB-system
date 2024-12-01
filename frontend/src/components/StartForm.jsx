import style from "../style.js";
import React from "react";
import { useNavigate } from "react-router";
import { useDispatch } from "react-redux";
import { setName } from "../reducer/profile.js";

const StartForm = () => {
  const navigate = useNavigate();
  const dispatch = useDispatch();

  const onUserClick = (event) => {
    console.log("User clicked");
    dispatch(setName("Рядовой обыватель"));
    navigate("auth/user");
  };

  const onRedactorClick = (event) => {
    console.log("Redactor clicked");
    dispatch(setName("Сержант редактор"));
    navigate("auth/redactor");
  };

  const onAdminClick = (event) => {
    console.log("Admin clicked");
    dispatch(setName("Генеральный генерал"));
    navigate("auth/administrator");
  };

  return (
    <div>
      <p style={style.textCentered}>
        <h3>
          Добро пожаловать в сервис отслеживания Aruco меток <br />
          Выберите профиль:
        </h3>
      </p>
      <div style={style.justifiedContent}>
        <button style={style.button} onClick={onUserClick}>
          Пользователь
        </button>
        <button style={style.button} onClick={onRedactorClick}>
          Редактор
        </button>
        <button style={style.button} onClick={onAdminClick}>
          Администратор
        </button>
      </div>
    </div>
  );
};

export default StartForm;
