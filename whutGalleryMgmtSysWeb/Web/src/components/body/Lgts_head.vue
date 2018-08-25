<template>
    <div class="lgts-header">
      <i class="logo" @click="goMain"></i>
      <div class="nav-warp">
        <router-link :to="item.route" class="head-text" v-for="(item,index) in nav_lists" :key="index">{{item.title}}</router-link>
      </div>
      <div class="header-left">
        <div class="search-box">
          <label for="search"><i class="search-label" @click="startSearch"></i></label>
          <input type="search" autocomplete="off" id="search" name="search" v-model="search_content" class="input-search"
                 :class='{ "search-now" : isS,"search-not":!isS}' @keyup.enter="startSearch" />
        </div>
      <div class="person-img-wrap" @mouseenter="showOptions" @mouseleave="unShowOptions" v-if="user_image" >
        <i :style="{'background-image':`url(${user_image})`,'background-size':'100% 100%','background-position':'center'}" @click="getInPerson" class="person-img"></i>
        <div class="user-option-wrap" v-if="show_option">
          <span class="user-option user-option-active">{{username}}</span>
          <span class="user-option" @click="getInPerson">个人主页</span>
          <span class="user-option" @click="showUserEdit">修改资料</span>
          <span class="user-option" @click="logout">退出</span>
        </div>
      </div>
        <div v-if="!user_image" class="go-login" title="点击登陆" @click="goLogin">登录</div>
      </div>
    </div>
</template>

<script>
  import {goLogin} from "../../utils/user";

  var index=0
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
      if(!this.$store.state.user.userInfo)
        this.$store.dispatch('GetUserInfo').then(()=>{
          console.log('个人信息获取成功')
        }).catch(()=>{
          console.log('获取个人信息失败')
        })
    },
      methods:{
        getInPerson(){
          this.$router.push('/tslg/person')
        },
        startSearch(){
          if(index===0){
            index=1
            this.isS=!this.isS
          }
          else{
            if(this.search_content===''){
              this.isS=!this.isS
              return
            }
            if(this.$router.currentRoute.name!=='main')
            this.$router.push('/tslg/main')
            this.$store.commit('SET_STATUS','special')
            this.$store.commit('SET_NEXT_SEARCH',`search=${this.search_content}&page=1`)
            this.$store.commit('SET_IMAGEGROUP')
            this.$store.dispatch('setImageGroupT').then(()=>{
              if(!this.$store.state.imageGroup.image.length)
                this.$store.commit('SET_NO_RESULT',true)
              this.$store.commit('SET_SEARCH_CONTEXT',this.search_content)
              this.search_content=''
            })
            index=0
            this.isS=!this.isS
          }
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
        }
      },
    }
</script>

<style scoped>

  .lgts-header{
    display: flex;
    height:5rem;
    width: 100%;
    background-color: #F6FAFB;
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
    width: 5rem;
    overflow: hidden;
    justify-content: center;
    align-items: center;
    cursor: pointer;
  }
  .person-img{
    width: 3rem;
    height: 3rem;
    -webkit-border-radius: 50%;
    -moz-border-radius: 50%;
    border-radius: 50%;
  }

  .active_nav{
    color: #9AD3E2;
  }
  .user-option-wrap{
    width: 8rem;
    display: flex;
    flex-direction: column;
    justify-content: flex-start;
    background: white;
    position: absolute;
    right: 2rem;
    top:5rem;
    z-index: 2;
  }

  .user-option{
    display: inline-block;
    width: 100%;
    height: 4rem;
    line-height: 4rem;
    text-align:left;
    text-indent: 1rem;
    font-size: 1.125rem;
    color: #4a4a4a;
    border-bottom: 1px solid #e9e9e9;
  }

  .user-option-active{
    color: #000;
    font-weight: bolder;
  }

  .user-option:hover{
    color: #5bc3dc;
  }

  .search-label {
    cursor: pointer;
    position: absolute;
    width: 3rem;
    height: 3rem;
    border-radius: 3rem;
    -webkit-border-radius:3rem;//适配以webkit为核心的浏览器(chrome、safari等)
    -moz-border-radius:3rem;//适配firefox浏览器
    text-indent: 1.5rem;
    border: 1px solid #cecece;
    background: url(../../assets/search.png) no-repeat center white;
    background-size: 1.2rem 1.2rem;
  }

  .search-box {
    height: 5rem;
    padding: 1rem;
    position: absolute;
    right: 10rem;
    top: 0;
  }
  .input-search{
    transition: all 0.3s;
    border-radius: 3rem;
  }

  .search-not {
    width: 0;
  }
  .search-now {
    width: 15rem;
    height: 100%;
    background-position: 1.2rem center;
    text-indent: 3rem;
    font-size: 1.5rem;
    padding-left: 0.3rem;
    border: 1px solid #cecece;
  }

  .go-login{
    font-size: 1.4rem;
    cursor: pointer;
    height: 3rem;
    width: 5rem;
    border: 0.0625rem solid #cecece;
    line-height: 3rem;
    border-radius: .5rem;
  }
  .go-login:hover{
    background: #fff;
  }
  input[type=search]::-webkit-input-placeholder {
    color: blue;
  }

  input[type=search]::-webkit-search-cancel-button {
    -webkit-appearance: none;
  }

  input[type=search]::-webkit-search-cancel-button {
    -webkit-appearance: none;
    position: relative;
    height: 1.25rem;
    width:  1.25rem;
    border-radius: 50%;
    margin-right: 1.2rem;
    background-color: #EBEBEB;
  }

  input[type=search]::-webkit-search-cancel-button:after {
    position: absolute;
    content: 'x';
    left: 25%;
    top: -12%;
    font-size: 1.25rem;
    color: #000;
  }

</style>
