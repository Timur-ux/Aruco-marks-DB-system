import "./App.css";
import { BrowserRouter as Router, Routes, Route } from "react-router-dom";

import style from "./style.js";
import Profile from "./components/Profile";
import StartForm from "./components/StartForm";
import AuthForm from "./components/AuthForm";
import RequestListForm from "./components/RequestListForm";
import TableGenerator from "./components/TableGenerator";

const App = () => {
  return (
    <div style={style.mainBlock}>
      <Router>
        <div style={{ ...style.mainForm, ...style.centered }}>
          <Routes>
            <Route path="/" element={<StartForm />} />
            <Route path="auth">
              <Route path=":access" element={<AuthForm />} />
            </Route>
            <Route path="profile" element={<Profile />}>
              <Route path="requests" element={<RequestListForm />} />
              <Route
                path="table_display"
                element={<TableGenerator />}
              />
            </Route>
          </Routes>
        </div>
      </Router>
    </div>
  );
};

export default App;
