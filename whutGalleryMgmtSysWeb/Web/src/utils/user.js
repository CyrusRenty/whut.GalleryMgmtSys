import {download, setUnLike,ApiSetLike} from "../api/action";
import store from '../store'
import router from '../router'
import cookie from './cookie'
import axios from './axios'


export function setImageInfo(id) {
  const {href} = router.resolve({
    name: 'image',
    params: {
      id:id
    }
  })
  window.open(href, '_blank')
}
export function setDownload(item){
  let data=new FormData
  data.append('image',item.id)
  let config={
    headers:{
      responseType: 'blob'
    }
  }
  axios.post(`/api/download/`,data,config).then((res)=>{
    let blob=new Blob([res.data])
    let url =window.URL.createObjectURL(blob)
    console.log(blob)
    let link = document.createElement('a');
    link.style.display = 'none';
    link.href = url;
    link.download=item.name+'.'+item.pattern
    document.body.appendChild(link);
    console.log(link)
    link.click();
    window.URL.revokeObjectURL(link.href);
  })
  // download(data).then((res)=>{
  //   let blob=new Blob([res.data])
  //   // let objectUrl = URL.createObjectURL(blob);
  //  //  console.log(objectUrl)
  //  // window.location.href = objectUrl;
  //   let url =window.URL.createObjectURL(blob)
  //   console.log(url)
  //   let link = document.createElement('a')
  //   link.style.display = 'none'
  //   link.href = url
  //   link.download=item.name+'.'+item.pattern
  //   //link.setAttribute('download', '123')
  //   document.body.appendChild(link)
  //   link.click()
  //   window.URL.revokeObjectURL(link.href);
  // })
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
  store.commit('SET_CUR_ROUTER',router.currentRoute.fullPath);
  store.commit('SET_DO_LOGIN',true);
  router.push('/tslg/login')
}
export function goRegister() {
  store.commit('SET_DO_LOGIN',false);
  router.push({name:'login'})
}

export function checkLogin() {
  if(cookie.getCookie('token'))
    return true
  else{
    store.commit('SET_CUR_ROUTER',router.currentRoute.fullPath)
    router.push('/tslg/login')
  }
}
export function showCollect(id) {
  if(checkLogin()) {
    store.commit('SET_IMAGE_ID',id);
    store.commit('SET_COLLECT_LIST',id);
    store.commit('SET_COLLECT_SHOW');
    document.body.style.overflow = 'hidden';
  }
}
export function setLike(item) {
  if(checkLogin()){
    let data=new FormData();
    data.append('image',item.id);
    data.append('user',store.state.user.userInfo.id);
    if(!item.if_like){
      ApiSetLike(data).then((res)=>{
        item.if_like=res.data.id;
        item.like_nums++
      }).catch((error)=>{
        console.log(error)
      })
    }else{
      setUnLike(item.if_like).then(()=>{
        item.if_like=false;
        item.like_nums--
      })
    }
  }
}
