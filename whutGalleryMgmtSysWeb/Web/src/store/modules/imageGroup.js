import {getTypeImage, getImage, getOrderImage, getImageInfo, getComment} from "../../api/get";
import mock from '../../utils/mock'
const imageGroup={
  state:{
    status:'normal',
    image:[],//mock.photos.results,
    main_next_page:'ordering=add_time&page=1',
    next_search:'',
    main_search:true,
    search_context:'',
    continue_getImage:true,
    imageInfo:{},//mock.photos.results[0],
    image_userInfo:{},
    image_id:0,
    collect_item:'',
    atImageInfo:false,
    comment_list:[],//mock.comment,
    comment_next_page:'',
    no_result:false,
    search_content:'',
    search_count:0,
    title:[],
    image_main:'',
    next_cates:'',
    position:[]
  },
  mutations:{
    SET_IMAGEGROUPI:(state,data)=>{
      state.image=data.results
      state.search_count=data.count
      if(data.count===0)
        this.no_result=true
      else this.no_result=false
    },
    SET_IMAGEGROUP:(state)=>{
      state.image=[]
    },
    SET_IMAGE_INFO:(state,data)=>{
      state.imageInfo=data
    },
    SET_IMAGE_USER_INFO:(state,data)=>{
      state.image_userInfo=data
    },
    SET_IMAGE_ID:(state,data)=>{
      state.image_id=data
    },
    SET_MAIN_NEXT_PAGE:(state,data)=>{
      state.main_next_page=data
    },
    SET_CONTINUE:(state,data)=>{
      state.continue_getImage=data
    },
    SET_COLLECT_ITEM:(state,data)=>{
      state.collect_item=data
    },
    SET_NEXT_SEARCH:(state,data)=>{
      state.next_search=data
    },
    SET_STATUS:(state,data)=>{
      state.status=data
    },
    SET_MAIN_SEARCH:(state,data)=>{
      state.main_search=data
    },
    SET_AT_IMAGEINFO:(state,data)=>{
      state.atImageInfo=data
    },
    SET_COMMENT_LIST:(state,data)=>{
      state.comment_list.push(...data)
    },
    SET_COMMENT_NEXT_PAGE:(state,data)=>{
      state.comment_next_page=data
    },
    SET_NO_RESULT:(state,data)=>{
      state.no_result=data
    },
    SET_TITLE:(state,data)=>{
      state.title=data
    },
    SET_IMAGE_MAIN:(state,data)=>{
      state.image_main=data
    },
    SET_NEXT_CATES:(state,data)=>{
      state.next_cates=data
    },
    SET_POSITION:(state,data)=>{
      state.position=data
    }
  },
  actions:{
    setImageGroupT({commit,state}){
      return new Promise((resolve,reject)=>{
         getTypeImage(state.next_search).then(res=>{
           if(res.data){
             if(res.data.next===null){
               commit('SET_CONTINUE',false)
             }
             else{
               commit('SET_NEXT_SEARCH',res.data.next.split("111.231.230.54/")[1]);
             }
             commit('SET_IMAGEGROUPI',res.data);
             resolve()
           }else reject()
        }).catch(error=>{
          reject(error)
        })
      })
    },
    setImageGroupI({commit,state}){
      return new Promise((resolve,reject)=>{
        getOrderImage(state.main_next_page).then((res)=>{
          if(res.data){
            if(res.data.next===null)
              commit('SET_CONTINUE',false)
            else{
              commit('SET_MAIN_NEXT_PAGE',res.data.next.split("?")[1]);
            }
            commit('SET_IMAGEGROUPI',res.data.results);
            resolve()
          }else reject()
      }).catch(()=>{
        reject()
      })
      })
    },
    setCommentList({commit,state}){
      return new Promise((resolve,reject)=>{
        getComment(state.comment_next_page).then((res)=>{
          if(res.data){
            if(res.data.next)
              commit('SET_COMMENT_NEXT_PAGE',res.data.next.split("?")[1])
            else commit('SET_COMMENT_NEXT_PAGE',null)
            commit('SET_COMMENT_LIST',res.data.results)
            resolve()
          }
          else
            reject()
        }).catch((error)=>{
          console.log(error)
        })
      })
    },
    setImageInfo({commit,state}){
      return new Promise((resolve,reject)=>{
        getImageInfo(state.image_id).then((res)=>{
          if(res.data){
            res.data.image=res.data.image.split(".400x300")[0]
            let size=res.data.size/1024
            if(size>1024){
              size=size/1024
              size=size.toFixed(2)
              size=size+'M'
            }else{
              size=size.toFixed(2)
              size=size+'K'
            }
            res.data.size=size
            commit('SET_IMAGE_USER_INFO',res.data.user)
            commit('SET_IMAGE_INFO',res.data)
            resolve()
          }else reject()
        })
      })
    },
    setCates({commit,state}){
      return new Promise((resolve,reject)=>{
        getOrderImage(state.next_cates).then((res)=>{
          if(res.data){

            commit('SET_IMAGEGROUPI',res.data)
            resolve()
          }else reject()
        })
      })
    }
  },
}
export default imageGroup


