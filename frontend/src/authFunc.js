import { client } from "./client"
import { getSHA256Hash } from "boring-webcrypto-sha256"

const authFunc = access => async (login, password) => {
  console.log(password, await getSHA256Hash(password))
  const response = await client.get("/api/login", {params: {
    access: access,
    login: login,
    password: await getSHA256Hash(password),
  }})

  console.log("Auth response: ", response)
}

export const userAuth = authFunc("user")
export const redactorAuth = authFunc("redactor")
export const administratorAuth = authFunc("administrator")
