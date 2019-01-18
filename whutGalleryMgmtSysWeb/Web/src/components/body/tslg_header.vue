<template>
  <div>
    <div>
    <div class="tslg-header">
      <i class="logo" @click="goMain"><a href="http://118.24.96.186/tslg/main"></a> </i>
      <div class="nav-warp">
        <router-link :to="item.route" class="head-text" v-for="(item,index) in nav_lists" :key="index">{{item.title}}</router-link>
      </div>
      <div class="header-left" >
      <div class="person-img-wrap" @mouseenter="showOptions" @mouseleave="unShowOptions" v-if="user_image&&!is_login" >
        <i :style="{'background-image':`url(${user_image})`,'background-size':'100% 100%','background-position':'center'}" @click="getInPerson" class="person-img"></i>
        <div class="username"> {{username}}</div>
        <div class="user-option-wrap" v-if="show_option">
          <span class="user-option" @click="getInPerson">个人主页</span>
          <span class="user-option" @click="showUserEdit">修改资料</span>
          <span class="user-option" @click="goUpload">上传</span>
          <span class="user-option" @click="logout">退出</span>
        </div>
      </div>
        <div v-if="!user_image||is_login" class="headLink">
          <a @click="goLogin">登录</a>
          <a class="borderSpan" @click="goRegister">注册</a>
        </div>
      </div>
    </div>
    <div class="search" ref="search" v-if="this.$router.currentRoute.name==='main'">
      <div v-if="!set_top" class="classify" @mouseenter="showClassifyCard" @mouseleave="showClassifyCard"><i></i>分类
        <ul v-if="show_title">
          <li v-for="(item,index) in classify" @click="goBCates(item.name,index)" @mouseenter="showClassifyCard1(index)" @mouseleave="showClassifyCard1(-1)">
            <span class="item-wrap"><span>{{item.name}}</span><i v-if="item.kids"></i></span>
          <ul v-if="index===show_title1">
            <li v-for="(item1,index1) in item.kids" @click.stop="goSCates(item1.name,index,index1)" @mouseenter="showClassifyCard2(index1)" @mouseleave="showClassifyCard2(-1)">
              <span class="item-wrap"><span>{{item1.name}}</span><i v-if="item1.kids"></i></span>
            <ul v-if="index1===show_title2">
              <li v-for="(item2,index2) in item1.kids" @click.stop="goLCates(item2.name,index,index1,index2)"><span>{{item2.name}}</span></li>
            </ul>
            </li>
          </ul>
          </li>
        </ul>
      </div>
      <input id="search" type="text" placeholder="请输入关键字查询"  @keyup.enter="startSearch" v-model="search_content" autocomplete="none"/>
      <label for="search" class="label" @click="startSearch"></label>
    </div>
    </div>
    <div class="tslg-header-top" ref="search" v-if="set_top&&$router.currentRoute.meta.search">
        <i class="logo" @click="goMain"><a href="http://111.231.230.54/tslg/main"></a> </i>
        <div class="search-top">
          <div class="classify classify1" @mouseenter="showClassifyCard" @mouseleave="showClassifyCard"><i></i>分类
            <ul v-if="show_title">
              <li v-for="(item,index) in classify" @click.stop="goBCates(item.name,index)" @mouseenter="showClassifyCard1(index)" @mouseleave="showClassifyCard1(-1)">
                <span class="item-wrap"><span>{{item.name}}</span><i v-if="item.kids"></i></span><span>{{item.name}}</span>
                <ul v-if="index===show_title1">
                  <li v-for="(item1,index1) in item.kids" @click.stop="goSCates(item1.name,index,index1)" @mouseenter="showClassifyCard2(index1)" @mouseleave="showClassifyCard2(-1)">
                    <span class="item-wrap"><span>{{item1.name}}</span><i v-if="item1.kids"></i></span>
                    <ul v-if="index1===show_title2">
                      <li v-for="(item2,index2) in item1.kids" @click.stop="goLCates(item2.name,index,index1,index2)"><span>{{item2.name}}</span></li>
                    </ul>
                  </li>
                </ul>
              </li>
            </ul>
          </div>
          <input id="search1" type="text" placeholder="请输入关键字查询"  @keyup.enter="startSearch" v-model="search_content"/>
          <label for="search1" class="label" @click="startSearch"></label>
        </div>
        <div class="header-left">
          <div class="person-img-wrap" @mouseenter="showOptions" @mouseleave="unShowOptions" v-if="user_image&&!is_login" >
            <i :style="{'background-image':`url(${user_image})`,'background-size':'100% 100%','background-position':'center'}" @click="getInPerson" class="person-img"></i>
            <div class="username"> {{username}}</div>
            <div class="user-option-wrap" v-if="show_option">
              <span class="user-option" @click="getInPerson">个人主页</span>
              <span class="user-option" @click="showUserEdit">修改资料</span>
              <span class="user-option" @click="goUpload">上传</span>
              <span class="user-option" @click="logout">退出</span>
            </div>
          </div>
          <div v-if="!user_image||is_login" class="headLink">
            <a @click="goLogin">登录</a>
            <a class="borderSpan" @click="goRegister">注册</a>
          </div>
        </div>
    </div>
    <edit-profile ref="edit"/>
  </div>
</template>

<script>
  import {goLogin, goRegister, setTitle} from "../../utils/user";

  import editProfile from '../editProfile'
  import cookie from '../../utils/cookie'
  import {getAllTitle} from "../../api/get";
  export default {
      name: "Lgts_head",
      components:{
          editProfile
      },
      data(){
        return {
          is_login:false,
          show_option:false,
          nav_lists:[
            {title:'首页',route:'/tslg/main'},
            {title:'排行榜',route:'/tslg/ranking_list'},
            {title:'签约摄影师',route:'/tslg/signed_list'}
          ],
          search_content:'',
          set_top:false,
          show_title:false,
          show_title1:-1,
          show_title2:-1,
          classify:[]
        }
      },
    computed:{
      user_image(){
        return this.$store.state.user.userInfo.image
      },
      username(){
        return this.$store.state.user.userInfo.username
      },
      // classify(){
      //   return this.$store.state.imageGroup.title
      // }
    },
    created(){
        if(this.$router.currentRoute.meta.search)
        getAllTitle().then((res)=>{
          this.classify=res.data;
          this.$store.commit('SET_TITLE',res.data)
        })
    },
    mounted(){
      window.addEventListener('scroll',this.setSearchTop)
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
          this.$refs.edit.showEdit()
        },
        logout(){
          cookie.delCookie('token');
          cookie.delCookie('user_id')
          this.is_login=true
        },
        goLogin(){
          goLogin()
        },
        goMain(){
          this.$router.push('/tslg/main')
        },
        goRegister(){
          goRegister()
        },
        showClassifyCard(){
          this.show_title=!this.show_title
        },
        showClassifyCard1(index){
          this.show_title1=index
        },
        showClassifyCard2(index){
          this.show_title2=index
        },
        startSearch(){
          if(!this.search_content)
            return
          const {href}=this.$router.resolve({
            name:'search_result',
            params:{search_content:this.search_content}
          })
          window.open(href,'_blank')
        },
        setSearch(text){
          this.search_content=text;
          this.startSearch()
        },
        setSearchTop(){
          if(document.documentElement.scrollTop>140)
            this.set_top=true
          else
            this.set_top=false
        },
        goSCates(item,index,index1){
          let s_index=[index,index1]
          this.goCates(item,s_index)
        },
        goLCates(item,index,index1,index2){
          let s_index=[index,index1,index2]
          this.goCates(item,s_index)
        },
        goBCates(item,index){
          let s_index=[index]
          this.goCates(item,s_index)
        },
        goCates(item,index){
          const {href}=this.$router.resolve({
            path:'cates',
            query:{
              cate:item,
              index:index
            }
          })
          window.open(href,'_blank')
        },
        goUpload(){
          this.$router.push({name:'doUpload'})
        }
      },
    }
</script>

<style lang="scss" scoped>
  @import "../../styles/variables";
  .tslg-header,.tslg-header-top{
    display: flex;
    height: 4rem;
    width: 100%;
    background-color: #fefefe;
    box-sizing: border-box;
    padding: 0 2.625rem;
    justify-content: center;
    align-items: center;
    border-bottom:0.0625rem solid #e9e9e9;
  }
  .tslg-header-top{
    position: fixed;
    top: 0;
    left: 0;
    z-index: 3;
    height: 4rem;
  }
  .logo{
    position: absolute;
    left: 3rem;
     background: url(../../assets/logo.svg);
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
     color:$normal;
   }
  .header-left{
    position: absolute;
    right: 3rem;
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
    color: $normal;
  }
  .user-option-wrap{
    position: absolute;
    width: 7.5rem;
    display: flex;
    flex-direction: column;
    background: #fff;
    left: 0;
    top:4rem;
    z-index: 99;
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
    color: $normal;
  }
  .headLink a{
    font-size:1.5rem;
    padding:0 0.5rem;
    cursor:pointer;
  }
  .headLink a.borderSpan{
    border-left:0.0625rem solid #000;
  }
  .username{
    /*font-weight: 600;*/
    margin-left: .5rem;
    font-size: 1.5rem;
  }
  .search{
    height: 3.5rem;
    display: flex;
    justify-content: center;
    align-items: center;
    width: 100%;
    margin: 1.5rem 0;
  }
  .search-top{
    height: 3rem;
    width: 52.5625rem;
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-left: .5rem;
  }
  .classify{
    height: 100%;
    width: 6rem;
    background: #eaeaea;
    position: relative;
    font-size: 1.25rem;
    padding:0 1rem;
    line-height: 2.5rem;
    display: flex;
    justify-content: center;
    align-items: center;
    cursor: pointer;
  }
  .classify i{
    display: inline-block;
    height: 1.25rem;
    width: 1.125rem;
    background: url(../../assets/sort.png) no-repeat center;
    background-size: 100% 100%;
    margin-right: 0.25rem;
  }
  .classify ul{
    z-index: 2;
    position: absolute;
    top: 3.5rem;
    left: 0;
    font-size: 1.25rem;
    background: #fff;
    width:7.5rem;
    box-shadow:0 0 4px $f-light;
    ul{
      top: 0;
      left: 7.55rem;
      li{
        color: $f-deep;
        &:hover{
          color: $normal;
        }
      }
    }
  }
  .classify li{
    position: relative;
    height: 3rem;
    line-height: 3rem;
    &:hover{
      color: $normal;
    }
  }
  .item-wrap{
    position: relative;
    display: flex;
    justify-content: space-between;
    align-items: center;
    width: 100%;
    padding-left: .5rem;
    text-align: left;
    i{
      margin-right: .5rem;
      width: .5rem;
      height: .7rem;
      background: url(../../assets/right_arrow.png) center no-repeat;
      background-size: 100% 100%;
    }
  }
  .classify1 ul{
    top: 3rem;
  }

  #search,#search1{
    font-size: 1.25rem;
    height: 100%;
    border: 0.0625rem solid #cecece;
    width: 40.5625rem;
    text-indent: 1.5rem;
    background: #fff;
  }
  .label{
    width: 6rem;
    height: 100%;
    background:url(../../assets/search_white.png) no-repeat center $normal;
    background-size:37.5%;
    cursor: pointer;
    &:hover{
      background-color: $hover;
    }
  }

</style>
