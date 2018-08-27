<template>
    <div class="tslg-header">
      <i class="logo" @click="goMain"><a href="http://111.231.230.54/tslg/main"></a> </i>
      <div class="nav-warp">
        <router-link :to="item.route" class="head-text" v-for="(item,index) in nav_lists" :key="index">{{item.title}}</router-link>
      </div>
      <div class="header-left">
      <div class="person-img-wrap" @mouseenter="showOptions" @mouseleave="unShowOptions" v-if="user_image" >
        <i :style="{'background-image':`url(${user_image})`,'background-size':'100% 100%','background-position':'center'}" @click="getInPerson" class="person-img"></i>
        <div class="username"> {{username}}</div>
        <div class="user-option-wrap" v-if="show_option">
          <span class="user-option" @click="getInPerson">个人主页</span>
          <span class="user-option" @click="showUserEdit">修改资料</span>
          <span class="user-option" @click="logout">退出</span>
        </div>

      </div>
        <div v-if="!user_image" class="headLink">
          <a @click="goLogin">登录</a>
          <a class="borderSpan" @click="goRegister">注册</a>
        </div>
      </div>
    </div>
</template>

<script>
  import {goLogin, goRegister} from "../../utils/user";

  import editProfile from '../editProfile'
  import cookie from '../../utils/cookie'
  export default {
      name: "Lgts_head",
      components:{
          editProfile
      },
      data(){
        return {
          search_content:'',
          isS:false,
          show_option:false,
          showEdit:false,
          nav_lists:[
            {title:'首页',route:'/tslg/main'},
            {title:'排行榜',route:'/tslg/ranking_list'},
            {title:'签约摄影师',route:'/tslg/signed_list'}
          ],
        }
      },
    computed:{
      user_image(){
        return this.$store.state.user.userInfo.image
      },
      username(){
        return this.$store.state.user.userInfo.username
      }
    },
    created(){
        if(cookie.getCookie('user_id')){
          if(!this.$store.state.user.userInfo)
            this.$store.dispatch('GetUserInfo').then(()=>{
              console.log('个人信息获取成功')
            }).catch(()=>{
              console.log('获取个人信息失败')
            })
        }
    },
      methods:{
        getInPerson(){
          this.$router.push('/tslg/person')
        },
        showOptions(){
          this.show_option=true
        },
        unShowOptions(){
          this.show_option=false
        },
        showUserEdit(){
          this.$router.push('/tslg/main/editProfile')
        },
        logout(){
          cookie.delCookie('token');
          cookie.delCookie('user_id')
          goLogin()
        },
        goLogin(){
          goLogin()
        },
        goMain(){
          this.$router.push('/tslg/main')
        },
        goRegister(){
          goRegister()
        }
      },
    }
</script>

<style scoped>

  .tslg-header{
    display: flex;
    height:4rem;
    width: 100%;
    background-color: #F7FAFB;
    box-sizing: border-box;
    padding: 0 2.625rem;
    justify-content: space-between;
    align-items: center;
    border-bottom:1px solid #cecece;
  }
  .logo{
     background: url(../../assets/header_logo.png);
     background-size: cover;
     height: 1.875rem;
     width: 6.4rem;
   }
  .logo a{
    display: block;
    height: 100%;
    cursor: pointer;
  }
  .nav-warp{
    display: flex;
    justify-content: center;
    min-width: 5rem;
  }
  .head-text{
     font-size: 1.5rem;
     margin-right: 2rem;
   }
  .router-link-active{
     color: #9ad4e2;
   }

  .person-img-wrap{
    display: flex;
    height: 5rem;
    overflow: hidden;
    justify-content: center;
    align-items: center;
    cursor: pointer;
  }
  .person-img{
    width: 2.5rem;
    height: 2.5rem;
    -webkit-border-radius: 50%;
    -moz-border-radius: 50%;
    border-radius: 50%;
  }

  .active_nav{
    color: #9AD3E2;
  }
  .user-option-wrap{
    width: 7.5rem;
    height: 9rem;
    display: flex;
    flex-direction: column;
    background: white;
    position: absolute;
    right: 2rem;
    top:4rem;
    z-index: 2;
    padding: 0 1.1875rem;
  }

  .user-option{
    display: inline-block;
    width: 100%;
    height: 3rem;
    line-height: 3rem;
    text-align:left;
    font-size: 1.125rem;
  }

  .user-option-active{
    color: #000;
    font-weight: bolder;
  }

  .user-option:hover{
    color: #9ad3e2;
  }
  .headLink a{
    font-size:1.5rem;
    padding:0 0.5rem;
    cursor:pointer;
  }
  .headLink a.borderSpan{
    border-left:0.0625rem solid #000;
  }
  .tslg-header .username{
    /*font-weight: 600;*/
    margin-left: .5rem;
    font-size: 1.5rem;
  }

</style>
