import axios from '../utils/axios'
let api='/api'
export function ApiSetLike(data) {
  return axios.post(`${api}/like/`,data)
}
export function setUnLike(image_id) {
  return axios.delete(`${api}/like/${image_id}/`)
}
export function setFollow(data) {
  return axios.post(`${api}/follow/`,data)
}
export function setUnFollow(data) {
  return axios.delete(`${api}/follow/${data}/`)
}
export function download(data) {
  return axios.post(`${api}/download/`,data)
}
export function sendAgree(data) {
  return axios.post(`${api}/application/`,data)
}
export function sendUserInfo(id,data) {
  return axios.put(`${api}/application/${id}/`,data)
}
export function getSignStatus() {
  return axios.get(`${api}/application/`)
}
export function changeFolderName(id,name) {
  return axios.put(`${api}/folders/${id}/`,name)
}
export function deleteFolder(id) {
  return axios.delete(`${api}/folders/${id}/`)
}
export function certification(data) {
  return axios.post(`${api}/certification/`,data)
}
export function likeComment(data) {
  return axios.post(`${api}/like_comment/`,data)
}
export function unLikeComment(id) {
  return axios.delete(`${api}/like_comment/${id}/`)
}

//下载管理修改记录
export function changeHis(id,data) {
  return axios.put(`${api}/images/${id}/`,data)
}
