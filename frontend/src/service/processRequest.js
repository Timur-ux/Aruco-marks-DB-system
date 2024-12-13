import { client } from "./client";

const processRequest = (type, uri, data) => {
  console.log("ProcessRequest: arg: type: ", type)
  console.log("ProcessRequest: arg: uri: ", uri)
  console.log("ProcessRequest: arg: data: ", data)

  if(type == "GET")
    return client.get(uri, {params: data, withCredentials: true})
  else if(type == "POST")
    return client.post(uri, data, {withCredentials: true})
  else if(type == "PUT")
    return client.put(uri, data, {withCredentials: true})
  else if(type == "DELETE")
    return client.delete(uri, {data: data, withCredentials: true})
  else
    console.log("Unsupported type: ", type)
  return new Promise()
}

export default processRequest;
