import { client } from "./client";


const fetchRequests = async (access) => {
  const response = await client.get("/api/requests", {params: {
    access: access
  }, withCredentials: true});

  if(response.status != 200) {
    console.log("Error: while fetching requests list. Response: ", response)
    return []
  }
  return response.data;
};


export default fetchRequests;
