import axios from "axios";

const addresses = {
  backend: "http://localhost:5000"
};

export const client = axios.create({baseURL: addresses.backend})
export const dummy = () => {}; // used for update elements by useEffect hook after data recieving in async functions

export default addresses;
