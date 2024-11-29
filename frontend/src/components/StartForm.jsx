import style from "../style.js";
import React from "react";
import { useNavigate } from "react-router";
import { setRequests } from "../reducer/requests.js";
import { useDispatch } from "react-redux";

const StartForm = () => {
  const navigate = useNavigate();
  const dispatch = useDispatch();

  dispatch(setRequests({
    requests: [
      {label: "Получить все марки",
        uri: "/api/marks"
      },
      {
        label: "Получить всех пользователей",
        uri: "/api/users"
      },
      {
        label: "Получить все действия пользоваетелей",
        uri: "/api/users/actions"
      }
    ]
  }));

  const onUserClick = (event) => {
    console.log("User clicked");
    navigate("Auth", {
      state: {
      profileName: "Рядовой обыватель",
      access:"user",
    }
    });
  };

  const onRedactorClick = (event) => {
    console.log("Redactor clicked");
    navigate("Auth", {
      state: {
      profileName: "Сержант редактор",
      access:"redactor",
    }
    });
  };

  const onAdminClick = (event) => {
    console.log("Admin clicked");
    navigate("Auth", {
      state: {
      profileName: "Генеральный генерал",
      access:"administrator",
    }
    });
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
        <h3>
          Добро пожаловать в сервис отслеживания Aruco меток <br />
          Выберите профиль:
        </h3>
      </p>
      <div style={style.justifiedContent}>
        <button style={style.mainForm} onClick={onUserClick}>Пользователь</button>
        <button style={style.mainForm} onClick={onRedactorClick}>Редактор</button>
        <button style={style.mainForm} onClick={onAdminClick}>Администратор</button>
      </div>
    </div>
  );
}

export default StartForm;
