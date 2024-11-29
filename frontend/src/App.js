import "./App.css";
import style from "./style.js";
import StartForm from "./components/StartForm";
import { BrowserRouter as Router, Routes, Route} from "react-router-dom";
import AuthForm from "./components/AuthForm";
import RequestListForm from "./components/RequestListForm";

const App = () => {
  return (
    <div style={style.mainBlock}>
    <Router>
      <Routes>
        <Route path="/" element={<StartForm/>} />
        <Route path="/Auth" element={<AuthForm />} />
        <Route path="/requests" element={<RequestListForm />} />
      </Routes>
    </Router>
    </div>
  );
};

export default App;
