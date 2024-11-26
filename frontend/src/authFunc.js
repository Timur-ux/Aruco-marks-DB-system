import { client } from "./client"

const authFunc = access => async (login, password) => {
  const response = await client.get("/api/login", {params: {
    access: access,
    login: login,
    password: password,
  }})

  console.log("Auth response: ", response)
}

export const userAuth = authFunc("user")
export const redactorAuth = authFunc("redactor")
export const administratorAuth = authFunc("administrator")
