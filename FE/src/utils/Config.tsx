export const axiosConfig = {
  headers: {
     Authorization: "Bearer " + sessionStorage.getItem("jwt_token")
  }
}
export const API = "http://localhost:8000"