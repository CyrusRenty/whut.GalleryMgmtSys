import Vue from 'vue'
import store from '../store'
import Router from 'vue-router'
import cookie from '../utils/cookie'

Vue.use(Router)

const router=new Router({
  mode:'history',
  routes: [
    {
      path: '/tslg',
      name:'tslg',
      component:()=>import('../views/tslg'),
      redirect:'/tslg/main',
      children:[
        {
          path:'login',
          name: 'login',
          meta:'登录-图说理工',
          component: ()=>import('../views/lgts_login')
        },
        {
          path:'main',
          name:'main',
          component:()=>import('../views/Lgts_main'),
          children:[

            {
              path:'editProfile',
              name:'editProfile',
              component:()=>import('../components/editProfile')
            }
          ]
        },
        {
          path:'image/:id',
          name:'image',
          component:()=>import('../components/Lgts_image_info'),
        },
        {
          path:'ranking_list',
          name:'ranking_list',
          component:()=>import('../views/person_card/ranking_list')
        },
        {
          path:'signed_list',
          name:'signed_list',
          component:()=>import('../views/person_card/signed_list')
        },
        {
          path:'person',
          name:'person',
          redirect:'/tslg/person/upload',
          component:()=>import('../views/person/Lgts_person'),
          children:[
            {
              path:'sign',
              name:'sign-nav',
              component:()=>import('../views/person/sign/sign')
            },
            {
              path:'download',
              name:'person_download',
              meta:'个人中心-图说理工',
              component:()=>import('@/views/person/main_content/download'),
            },
            {
              path:'folder_content',
              name:'folder_content',
              meta:'个人中心-图说理工',
              component:()=>import('@/views/person/main_content/folder_content'),
            },
            {
              path:'collection',
              name:'person_collection',
              meta:'个人中心-图说理工',
              component:()=>import('@/views/person/main_content/collection'),
            },
            {
             path: 'upload',
             name: 'person_upload',
              meta:'个人中心-图说理工',
             component:()=> import('@/views/person/main_content/person_upload'),
              children: [
                {
                  path: 'uploader',
                  name: 'uploader',
                  meta:'上传',
                  component:()=> import('../components/uploader'),
                }
              ]
            },
            ]
        },
        {
          path:'/tslg/other_user/:Id',
          name:'other_user',
          component:()=>import('../views/person/other_user/other_user'),
        },
        {
          path:'zcsm',
          name:'zcsm',
          meta:'注册声明-图说理工',
          component:()=>import('../views/zcsm')
        },
        {
          path:'search_result/:search_content',
          name:'search_result',
          component:()=>import('../views/search_result')
        }
      ]
    },
  ],
})
export default router
router.beforeEach((to,from,next)=>{
  if(to.meta.length)
    document.title=to.meta
  if(to.name==='other_user'&&store.state.user.other_next_page.indexOf('page=1')!==-1){
    let id=to.params.Id
    store.dispatch('setOtherUserInfo',id)
    store.dispatch('SetOtherUserImages')
  }
  if(!store.state.user.userInfo&&cookie.getCookie('user_id')){
    store.dispatch('GetUserInfo')
    if(to.name==='image'){
      store.commit('SET_IMAGE_ID',to.params.id)
      store.dispatch('setImageInfo').then(()=>{
        document.title=store.state.imageGroup.imageInfo.name
      })
    }
    if(to.name==='search_result'){
      store.commit('SET_SEARCH_CONTENT',to.params.search_content)
      document.title=to.params.search_content
    }
  }
  if(!cookie.getCookie('token')){
    if(to.name!=='zcsm'){
      if(to.name!=='main'&&to.name!=='login')
        router.push('/tslg')
    }
  }else store.commit('SET_TOKEN',true)
  console.log(to,from)
  next()
})

