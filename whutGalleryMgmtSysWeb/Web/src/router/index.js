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
          meta:{title:'登录-图说理工'},
          component: ()=>import('../views/tslg_login')
        },
        {
          path:'main',
          name:'main',
          meta:{search:true},
          component:()=>import('../views/Lgts_main'),
        },
        {
          path:'image/:id',
          name:'image',
          component:()=>import('../views/tslg_image_info'),
        },
        {
          path:'ranking_list',
          name:'ranking_list',
          component:()=>import('../views/rank/index')
        },
        {
          path:'signed_list',
          name:'signed_list',
          component:()=>import('../views/rank/signed_list')
        },
        {
          path:'person',
          name:'person',
          redirect:'/tslg/person/person_center',
          component:()=>import('../views/person/Lgts_person'),
          children:[
            {
              path:'person_center',
              redirect:'person_center/upload',
              component:()=>import('../views/person/person_center/index'),
              children:[
                {
                  path:'sign',
                  name:'sign',
                  component:()=>import('../views/person/sign/sign')
                },
                {
                  path:'follow',
                  name:'person_follow',
                  meta:{title:'个人中心-图说理工'},
                  component:()=>import('../views/person/person_center/main_content/follow'),
                },
                {
                  path:'folder_content',
                  name:'folder_content',
                  meta:{title:'个人中心-图说理工'},
                  component:()=>import('../views/person/person_center/main_content/folder_content'),
                },
                {
                  path:'collection',
                  name:'person_collection',
                  meta:{title:'个人中心-图说理工',card:true},
                  component:()=>import('../views/person/person_center/main_content/collection'),
                },
                {
                  path: 'upload',
                  name: 'person_upload',
                  meta:{title:'个人中心-图说理工',card:true},
                  component:()=> import('../views/person/person_center/main_content/person_upload'),
                }
                ]
            },
            {
              path:'person_works',
              component:()=>import('../views/person/person_works/index'),
              redirect:'/tslg/person/person_works/upload',
              children:[
                {
                  path:'upload',
                  name:'myUpload',
                  component:()=>import('../views/person/person_works/upload')
                },
                {
                  path:'download',
                  name:'myDownload',
                  component:()=>import('../views/person/person_works/download')
                }
              ]
            }
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
          meta:{title:'注册声明-图说理工'},
          component:()=>import('../views/zcsm')
        },
        {
          path:'search_result/:search_content',
          name:'search_result',
          meta:{search:true},
          component:()=>import('../views/search_result')
        },
        {
          path:'cates',
          name:'cates',
          meta:{search:true},
          component:()=>import('../views/search_result')
        },
        {
          path:'doUpload',
          name:'doUpload',
          meta:{search:true},
          component:()=>import('../views/upload/index')
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
  }
  if(to.name==='image'){
    store.commit('SET_IMAGE_ID',to.params.id)
    store.dispatch('setImageInfo').then(()=>{
      document.title=store.state.imageGroup.imageInfo.name
    })
  }
  if(to.name==='search_result'){
    document.title=to.params.search_content
  }
  if(to.name==='cates'){
    document.title=to.query.cate
  }
  // if(!cookie.getCookie('token')){
  //   if(to.name!=='zcsm'){
  //     if(to.name!=='main'&&to.name!=='login'){
  //       console.log(router)
  //       router.push('/tslg/login')
  //     }
  //   }
  // }else store.commit('SET_TOKEN',true)
  console.log(to,from)
  next()
})

