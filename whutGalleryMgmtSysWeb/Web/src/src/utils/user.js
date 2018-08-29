import {download} from "../api/action";
import store from '../store'
import router from '../router'
import cookie from './cookie'
import {getTypeImage,getTitle} from "../api/get";

export function setImageInfo(id) {
  const {href} = router.resolve({
    name: 'image',
    params: {
      id:id
    }
  })
  window.open(href, '_blank')
}
export function setDownload(id){
  let data=new FormData
  data.append('image',id)
  download(data).then((res)=>{
    let blob=new Blob([res.data],{type:'image/*'})
    console.log(blob)
    let objectUrl = URL.createObjectURL(blob);
    console.log(objectUrl)
   window.location.href = objectUrl;
   //  let url =window.URL.createObjectURL(blob)
   //  console.log(url)
   //  let link = document.createElement('a')
   //  link.style.display = 'none'
   //  link.href = url
   //  link.download='123.jpeg'
   //  //link.setAttribute('download', '123')
   //  document.body.appendChild(link)
   //  link.click()
   //  window.URL.revokeObjectURL(link.href);
  })
}
export function getInOtherUser(id){
  if(id===store.state.user.userInfo.id)
    router.push('/tslg/person')
  else{
    store.commit('SET_OTHER_NEXT_PAGE',`user=${id}&page=1`)
    store.commit('SET_OTHER_IMAGES_ENPTY')
    router.push({name:'other_user',params:{Id:id}})
  }
}
export function goLogin() {
  store.commit('SET_DO_LOGIN',true)
  router.push('/tslg/login')
}
export function goRegister() {
  store.commit('SET_DO_LOGIN',false)
  router.push({name:'login'})
}
export function setTitle() {
  var array=[]
  getTitle().then((res)=>{
    array=res.data
    for(let i=0;i<res.data.length;i++){
      array[i].image=[]
      getTypeImage(`group/${i+1}/?page=1&num=4`).then((res)=>{
        array[i].image=res.data.results
      })
    }
    store.commit('SET_TITLE',array)
  })
  return array
}
export function checkLogin() {
  if(cookie.getCookie('token'))
    return true
  else{
    store.commit('SET_CUR_ROUTER',router.currentRoute.fullPath)
    router.push('/tslg/login')
  }
}
