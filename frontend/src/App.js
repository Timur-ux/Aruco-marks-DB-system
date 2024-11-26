import "./App.css";
import style from "./style.js";
import StartForm from "./startForm";
import { BrowserRouter as Router, Routes, Route} from "react-router-dom";
import AuthForm from "./components/AuthForm";
import { administratorAuth, redactorAuth, userAuth } from "./authFunc";

const App = () => {
  return (
    <div style={style.mainBlock}>
    <Router>
      <Routes>
        <Route path="/" element={<StartForm/>} />
        <Route path="/user" element={<AuthForm profileName={"User"} processAuth={userAuth} />} />
        <Route path="/redactor" element={<AuthForm profileName={"Redactor"} processAuth={redactorAuth} />} />
        <Route path="/admin" element={<AuthForm profileName={"Administrator"} processAuth={administratorAuth} />} />
      </Routes>
    </Router>
    </div>
  );
};

export default App;
