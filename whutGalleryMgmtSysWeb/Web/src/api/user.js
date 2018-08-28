import axios from '../utils/axios'

let api='/api'
export function login(data) {
  return axios.post(`${api}/login/`, data)
}
export function register(data) {
  return axios.post(`${api}/users/`, data)
}
export function editProfile(data) {
  return axios.put(`${api}/users/`,data)
}
export function upload(data) {
  return axios.post(`${api}/images/`, data)
}
export function getUserInfo(user_id) {
  return axios.get(`${api}/users/${user_id}/`)
}
export function getRankImage(params) {
  return axios.get(`${api}/users/`)
}
export function addImage(data) {
  return axios.post(`${api}/collect/`,data)
}
export function deleteImage(id){
  return axios.delete(`${api}/collect/${id}/`)
}
export function newFolder(data) {
  return axios.post(`${api}/folders/`,data)
}
export function forgetPassword(data) {
  return axios.post(`${api}/forget/`,data)
}
export function changeUserInfo(id,data) {
  return axios.put(`${api}/users/${id}/`,data)
}
export function checkName(data) {
  return axios.get(`${api}/has_user/?username=${data}`)
}
export function checkEmail(data) {
  return axios.get(`${api}/has_user/?email=${data}`)
}
export function setComment(data) {
  return axios.post(`${api}/comment/`,data)
}
export function report(data) {
  return axios.post(`${api}/report/`,data)
}
