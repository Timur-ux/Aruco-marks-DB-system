import axios from "axios";

const addresses = {
  backend: "http://localhost:5000"
};

export const client = axios.create({baseURL: addresses.backend})

export default addresses;