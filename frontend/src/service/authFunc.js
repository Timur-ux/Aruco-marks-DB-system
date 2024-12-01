import { client } from "./client"
import { getSHA256Hash } from "boring-webcrypto-sha256"

export const authFunc = access =>
    async (login, password) => {
      const response = await client.post("/api/login",  {
        access: access.toLowerCase(),
        login: login,
        password: await getSHA256Hash(password),
      })
      return response;
    };

export const userAuth = authFunc("user")
export const redactorAuth = authFunc("redactor")
export const administratorAuth = authFunc("administrator")
