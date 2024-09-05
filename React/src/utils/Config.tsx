const getToken = () => {
  const s = sessionStorage.getItem("jwt_token")
  return s ? s : "{}"
}
export const axiosConfig = () => {
  return {
    headers: {
      Authorization: "Bearer " + JSON.parse(getToken()).access_token
    }
  }
}
export const API = "http://localhost:8000"