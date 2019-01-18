import {login ,getUserInfo,newFolder} from '../../api/user'
import {
  getFolderImage, getUploadHistory, getCollection, getDownloadHistory, getCollectList,
  getComment
} from "../../api/get";
import cookie from "../../utils/cookie";
import mock from '../../utils/mock'
const jwt=require('jsonwebtoken')

const user={
  state:{
    token:false,
    userInfo:'',
    show_collect:false,
    collect_list:[],//main
    upload_his:[],//mock.photos.results,
    folder_list:[],//person
    folder_images:{},
    download_his:[],
    other_user_images:[],
    download_next_page:'page=1',
    upload_next_page:'page=1',
    other_next_page:'page=1',
    if_continue:true,
    other_count:1,
    down_count:1,
    up_count:1,
    other_userInfo:{},
    doLogin:true,
    cur_router:''
  },
  mutations:{
    SET_TOKEN:(state,data)=>{
      state.token=data
    },
    SET_COLLECT_SHOW:(state)=>{
      state.show_collect=!state.show_collect
    },
    SET_USER_INFO:(state,data)=>{
      state.userInfo=data
    },
    SET_COLLECT_LIST:(state,image_id)=>{
      getCollectList(image_id).then((res)=>{
        state.collect_list=res.data
      }).catch((error)=>{
        console.log(error)
      })
    },
    ADD_FOLDER:(state,data)=>{
      newFolder(data).then(()=>{})
    },
    SET_UPLOAD_HIS:(state,data)=>{
      state.upload_his.push(...data.results)
      state.up_count=data.count
    },
    SET_FOLDER_LIST:(state,data)=>{
      state.folder_list=data;
    },
    SET_DOWNLOAD_HIS:(state,data)=>{
      state.download_his.push(...data.results)
      state.down_count=data.count
    },
    SET_FOLDER_IMAGES:(state,data)=>{
      state.folder_images=data
    },
    SET_OTHER_USER_IMAGES:(state,data)=>{
      state.other_user_images.push(...data.results)
      state.other_count=data.count
    },
    SET_OTHER_IMAGES_ENPTY:(state)=>{
      state.other_user_images=[]
    },
    SET_DOWNLOAD_NEXT_PAGE:(state,data)=>{
      state.download_next_page=data
    },
    SET_UPLOAD_NEXT_PAGE:(state,data)=>{
      state.upload_next_page=data
    },
    SET_OTHER_NEXT_PAGE:(state,data)=>{
      state.other_next_page=data
    },
    SET_IF_CONTINUE:(state,data)=>{
      state.if_continue=data
    },
    SET_COUNT:(state,data)=>{
      state.count=data
    },
    SET_OTHER_USER_INFO:(state,data)=>{
      state.other_userInfo=data
    },
    SET_DO_LOGIN:(state,data)=>{
      state.doLogin=data
    },
    SET_CUR_ROUTER:(state,data)=>{
      state.cur_router=data
    }
  },
  actions:{
    Login({commit},userInfo){
      return new Promise((resolve,reject)=>{
        login(userInfo).then((res)=>{
          if(res){
            cookie.delCookie('token')
            cookie.setCookie('token',res.data.token,7)
            commit('SET_TOKEN',true);
            cookie.delCookie('user_id')
            cookie.setCookie('user_id',jwt.decode(cookie.getCookie('token')).user_id,7)
            resolve()
          } else{
            reject()
          }
        }).catch(()=>{
          reject()
        })
      })
    },
    GetUserInfo({commit}){
      return new Promise((resolve,reject)=>{
        getUserInfo(cookie.getCookie('user_id')).then((res)=>{
          if(res.data){
            commit('SET_USER_INFO',res.data)
            resolve()
          }else reject()
        }).catch((error)=>{
          reject(error)
        })
      })
    },
    SetUploadHis({commit,state}){
      return new Promise((resolve,reject)=>{
         getUploadHistory(state.upload_next_page).then((res)=>{
           if(res.data){
             if(res.data.next===null)
               commit('SET_UPLOAD_NEXT_PAGE',null)
             else
               commit('SET_UPLOAD_NEXT_PAGE',res.data.next.split('?')[1])
             commit('SET_UPLOAD_HIS',res.data)
             resolve()
           }else reject()
        }).catch((error)=>{
          reject(error)
        })
      })
    },
    SetOtherUserImages({commit,state}){
      return new Promise((resolve,reject)=>{
        getUploadHistory(state.other_next_page).then((res)=>{
          if(res.data){
            if(res.data.next===null)
              commit('SET_OTHER_NEXT_PAGE',null)
            else
              commit('SET_OTHER_NEXT_PAGE',res.data.next.split('?')[1])
            commit('SET_OTHER_USER_IMAGES',res.data)
            resolve()
          }else reject()

        }).catch((error)=>{
          reject(error)
        })
      })
    },
    SetFolderList({commit}){
      return new Promise((resolve,reject)=>{
         getCollection().then((res)=>{
          commit('SET_FOLDER_LIST',res.data)
           resolve()
        }).catch((error)=>{
          reject(error)
        })
      })
    },
    SetDownLoadHis({commit,state}){
      return new Promise((resolve,reject)=>{
         getDownloadHistory(state.download_next_page).then((res)=>{
           if(res.data.next===null)
             commit('SET_DOWNLOAD_NEXT_PAGE',null)
           else
             commit('SET_DOWNLOAD_NEXT_PAGE',res.data.next.split('?')[1])
          commit('SET_DOWNLOAD_HIS',res.data)
           resolve()
        }).catch((error)=>{
              reject(error)
        })
      })
    },
    SetFolderImages({commit},id){
      return new Promise((resolve,reject)=>{
        getFolderImage(id).then((res)=>{
          if(res.data){
            commit('SET_FOLDER_IMAGES',res.data)
            resolve()
          }else reject()
        }).catch((error)=>{
          reject(error)
        })
      })
    },
    setOtherUserInfo({commit},id){
      getUserInfo(id).then((res)=>{
        if(res.data){
          commit('SET_OTHER_USER_INFO',res.data)
        }else reject()
        //   {
        //   getUserInfo(id).then((res)=>{
        //     if(res.data){
        //       commit('SET_OTHER_USER_INFO',res.data)
        //     }
        //   })
        // }
      }).catch((res)=>{console.log(res)})
    },
  },

}

export default user

