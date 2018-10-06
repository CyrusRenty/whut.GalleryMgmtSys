<template>
  <div class="home-page-body clear">
    <div class="home-page clear">
      <div class="cover-photo"></div>
      <!--登陆表单-->
      <form class="user-window" v-show="forget_state?(!forget_state):login_state">
        <div class="user-option" ref="loginForm">
          <a class="a-active" >登录</a>
          <a class="a-not-active border-a" @click="changeShow">注册</a>
        </div>
        <div class="window-form">
          <div class="user-input login-input">
            <input v-model="username" type="text" class="input-area" name='username' placeholder="用户名" @blur="checkNameExist" ref="log_username" @focus="inputFocus('log_username')"/>
            <div class="hint">{{hint_username}}</div>
            <input v-model="password" type="password" class="input-area" name="password" placeholder="密码" ref="log_password" @blur="unFocus('log_password')"  @focus="inputFocus('log_password')"/>
            <div class="hint">{{hint_password}}</div>
            <div class="yzm-box">
              <input v-model="yzm" type="text" class="input-area" placeholder="验证码" @input="checkYzm" ref="log_yzm" @focus="inputFocus('log_yzm')" @blur="unFocus('log_yzm')"/>
              <yzm v-on:yzmValue="getYzm" ref="yzm"/>
            </div>
            <div class="hint">{{hint_yzm}}</div>
          </div>
          <div class="checkbox remember-password-container clear">
            <input type="checkbox" id="remember-password-checkbox" @click="setRemember" ref="check_rmb">
            <label for="remember-password-checkbox">
              记住密码
            </label>
            <a class="return-to-another" @click="changeForget">忘记密码</a>
          </div>
          <div class="hint">{{hint_check}}</div>
          <div class="to-do-box">
            <input type="button" value="登录" class="to-do-btn" @click="login"/>
          </div>
        </div>
      </form>

      <!--注册表单-->
      <form class="user-window" v-show="forget_state?(!forget_state):!login_state" ref="signForm">
        <div class="user-option">
          <a class="a-not-active" @click="changeShow" onselectstart="return false;">登录</a>
          <a class="a-active border-a" onselectstart="return false;">注册</a>
        </div>
        <div class="window-form">
          <div class="user-input">
            <input type="text" v-model="username"  class="input-area" placeholder="用户名" ref="log_username" @focus="inputFocus('log_username')" @input="inputUserName"/>
            <div class="hint">{{hint_username}}</div>
            <input type="password" v-model="password" class="input-area" placeholder="密码" ref="log_password"  @focus="inputFocus('log_password')" @blur="checkPswLength"/>
            <div class="hint">{{hint_password}}</div>
            <input type="password" v-model="passwordAgain" class="input-area " placeholder="重复密码" ref="log_password_twice" @blur="checkSamePwd"  @focus="inputFocus('log_password_twice')"/>
            <div class="hint">{{hint_password_twice}}</div>
            <input type="text" v-model="email" name="email" class="input-area" placeholder="邮箱" ref="log_email" @blur="checkEmail" @focus="inputFocus('log_email')" />
            <div class="hint">{{hint_email}}</div>
            <div class="yzm-box">
              <input v-model="yzm" type="text" class="input-area" placeholder="验证码"  @input="checkYzm" ref="log_yzm" @focus="inputFocus('log_yzm')" @blur="unFocus('log_yzm')"/>
              <yzm v-if="!login_state" v-on:yzmValue="getYzm" ref="yzm"/>
            </div>
            <div class="hint">{{hint_yzm}}</div>
          </div>
          <div class="checkbox remember-password-container clear" @click="clickCheckbox" >
            <input type="checkbox" id="agree-declaration"  checked="checked" ref="agree_declaration"/>
            <label for="agree-declaration">我同意图说理工</label>
            <a class="a-zcsm" @click="goToZcsm">《注册声明》</a>
          </div>
          <div class="hint">{{hint_agree}}</div>
          <div class="hint">{{hint_check}}</div>
          <div class="to-do-box register-box">
            <input type="button" @click="login" value="注册" class="to-do-btn" ref="btn_register"/>
          </div>
        </div>
      </form>

      <!--找回密码表单-->
      <form class="user-window" v-if="forget_state" ref="forgetForm">
        <div class="user-option">
          <a class="a-active" @click="" onselectstart="return false;">找回密码</a>
          <a class="a-not-active border-a" @click="changeForget" onselectstart="return false;">返回登录</a>
        </div>
        <div class="window-form">
          <div class="user-input forget-input">
            <input type="text" v-model="email" class="input-area" placeholder="账号邮箱" name="email" ref="log_email" @blur="checkEmail" @focus="inputFocus('log_email')" />
            <div class="hint">{{hint_email}}</div>
            <div class="yzm-box">
              <input v-model="yzm" type="text" class="input-area" placeholder="验证码"  @input="checkYzm" ref="log_yzm" @focus="inputFocus('log_yzm')" @blur="unFocus('log_yzm')"/>
              <yzm v-on:yzmValue="getYzm" ref="yzm"/>
            </div>
            <div class="hint">{{hint_yzm}}</div>
          </div>
          <div class="hint">{{hint_check}}</div>
          <div class="to-do-box register-box">
            <input type="button" @click="whenForget()" value="重置密码" class="to-do-btn"/>
          </div>
        </div>
      </form>

    </div>
    <div class="copyright">
      Copyright©&nbsp;&nbsp;&nbsp;2018&nbsp;&nbsp;&nbsp;共青团武汉理工大学委员会宣传部
    </div>
  </div>
</template>

<script>
  import {register, forgetPassword, checkName, checkEmail} from "../api/user";
  import yzm from '../components/yzm'
  import cookie from "../utils/cookie";
  export default {
    name: "lgts_login",
    components: {
       yzm
    },
    data: function () {
      return {
        state: true,
        login_state: true,
        forget_state: false,
        username: '',
        password: '',
        hint_password_twice:'',
        passwordAgain: '',
        email: '',
        yzm: '',
        t_yzm: '',
        hint_username:'',
        hint_password:'',
        hint_yzm:'',
        hint_email:'',
        hint_check:'',
        hint_agree:'',
      }
    },
    created(){

    },
    mounted() {
      if(cookie.getCookie('check_remember')==='true'){
        this.$refs.check_rmb.checked=true
        this.username=cookie.getCookie('username')
        this.password=cookie.getCookie('password')
      }
      else  this.$refs.check_rmb.checked=false
      if(!this.$store.state.user.doLogin)
        this.login_state=false
    },
    methods: {
      //验证码获取
      getYzm(yzmValue){
        this.t_yzm=yzmValue
      },
      //登录或者注册账户
      login() {
        if(!this.username){
          this.hint_username='请输入用户名'
          this.$refs.log_username.style.border='#ff0000 0.0625rem solid'
          return
        }
        if(!this.password){
          this.hint_password='请输入密码'
          this.$refs.log_password.style.border='#ff0000 0.0625rem solid'
          return
        }
        if(!this.yzm||this.yzm!==this.t_yzm){
          this.hint_yzm='请输入验证码'
          this.$refs.log_yzm.style.border='#ff0000 0.0625rem solid'
          return
        }
          let data = new FormData();
          data.append('username', this.username)
          //let password=this.changePassword(this.password)
          data.append('password', this.password)
          if (this.login_state) {
              this.$store.dispatch('Login',data).then(()=>{
                let route=this.$store.state.user.cur_router
                  if(route){
                  this.hint_check='登录跳转中'
                    this.$router.push(route)
                    //this.$store.commit('SET_CUR_ROUTER','')
                  }else this.$router.push('/tslg/main')
                  if(this.$refs.check_rmb.checked)
                    this.doRememberPassword()
              }).catch(()=>{
                 this.hint_password='密码错误'
              })
          }
          else {
            if (!this.email) {
              this.hint_email = '请输入邮箱'
              this.$refs.log_email.style.border = '#ff0000 0.0625rem solid'
              return
            }
            if (!this.$refs.agree_declaration.checked) {
              this.hint_agree = '请勾选图说理工注册声明'
              return
            }
            data.append('email', this.email)
            this.hint_check = '发送邮件中'
            register(data).then((res) => {
              this.$refs.btn_register.style.disbled='disabled'
              if (res.data.non_field_errors) {
                this.hint_check = res.data.non_field_errors
              } else {
                if (res.data.id)
                  this.hint_check = '请前往邮箱确认'
                else this.hint_check = '发送失败'
              }
              setTimeout(() => {
                this.hint_check = ''
              }, 10000)
            })
          }
      },
      setRemember(){
        if(this.$refs.check_rmb.checked)
          cookie.setCookie('check_remember',true,30)
        else cookie.delCookie('check_remember')
      },
      doRememberPassword(){
        cookie.setCookie('username',this.username,30)
        cookie.setCookie('password',this.password,30)
      },
      //重置密码
      whenForget() {
        if(!this.yzm||this.yzm!==this.t_yzm){
          this.hint_yzm='请输入验证码'
          this.$refs.log_yzm.style.border='#ff0000 0.0625rem solid'
          this.redraw()
          return
        }
        if(!this.email){
          this.hint_email='请输入邮箱'
          this.$refs.log_email.style.border='#ff0000 0.0625rem solid'
          return
        }
        let data = new FormData();
        data.append('email', this.email)
        forgetPassword(data).then(() => {
          this.hint_check='请前往邮箱修改'
        })
      },
      clearInput(){
        this.username=''
        this.password=''
        this.passwordAgain=''
        this.yzm=''
        this.email=''
        this.hint_email=''
        this.hint_password=''
        this.hint_username=''
        this.hint_yzm=''
        this.hint_password_twice=''
        this.$refs.log_username.style.border='0.0625rem solid #cecece'
        this.$refs.log_yzm.style.border='0.0625rem solid #cecece'
        this.$refs.log_username.style.border='0.0625rem solid #cecece'
      },
      changeShow() {
        this.login_state = !this.login_state
        this.clearInput()
        this.redraw()
      },
      changeForget() {
        this.forget_state = !this.forget_state
        this.clearInput()
        this.redraw()
      },
      redraw() {
        this.yzm = ""
        this.$refs.yzm.handleDraw()
      },
      inputFocus(data){
        this.$refs[data].style.border='#82E6FF 0.0625rem solid'
      },
      unFocus(data){
        this.hint_password=''
        this.$refs[data].style.border='0.0625rem solid #cecece'
      },
      checkNameExist(){
        checkName(this.username).then((res)=> {
          if (!res.data.msg) {
            this.$refs.log_username.style.border = '#ff0000 0.0625rem solid'
            this.hint_username = '该用户名不存在'
          } else {
            if (res.data.status) {
              this.hint_username = '你的账号还未激活，请重新注册'
            } else {
              this.$refs.log_username.style.border = '0.0625rem solid #cecece'
              this.hint_username = ''
            }
          }
        })
      },
      checkYzm(){
        if(this.yzm.length===4){
          this.yzm = this.yzm.toUpperCase()
          if(this.yzm!==this.t_yzm){
            this.hint_yzm='验证码输入错误'
            this.$refs.log_yzm.style.border='0.0625rem solid #ff0000'
            this.redraw()
          }else{
            this.hint_yzm=''
            this.$refs.log_yzm.style.border='0.0625rem solid #cecece'
          }
        }
      },
      checkSamePwd(){
        if(this.passwordAgain.length){
          if(this.password!==this.passwordAgain){
            this.hint_password_twice='密码不一致 请重新输入'
            this.$refs.log_password.style.border='0.0625rem solid #ff0000'
            this.$refs.log_password_twice.style.border='0.0625rem solid #ff0000'
          }
          else{
            this.$refs.log_password.style.border='0.0625rem solid #cecece'
            this.$refs.log_password_twice.style.border='0.0625rem solid #cecece'
            this.hint_password_twice=''
          }
        }

      },
      checkEmail(){
        if(this.email.length){
          let re=/^[A-Za-z\d]+([-_.][A-Za-z\d]+)*@([A-Za-z\d]+[-.])+[A-Za-z\d]{2,4}$/
          if(!re.test(this.email)){
            this.hint_email='请输入正确邮箱'
            this.$refs.log_email.style.border='0.0625rem solid #ff0000'
          }else{
            this.hint_email=''
            this.$refs.log_email.style.border='0.0625rem solid #cecece'
          }
          checkEmail(this.email).then((res)=>{
            if(res.data.msg&&!res.data.status){
              this.hint_email='该邮箱已经被注册'
            }
          })
        }
      },
      inputUserName(){
        if(this.username.length>=6){
          let length=0
          for(var i=0;i<this.username.length;i++){
            var a=this.username.charAt(i)
            if (a.match(/[^\x00-\xff]/ig) != null){
              length+=2
            }else length+=1
          }
          if(length>12){
            this.hint_username='用户名过长'
            this.$refs.log_username.style.border='#ff0000 0.0625rem solid'
          }else{
            this.hint_username=''
            this.$refs.log_username.style.border='0.0625rem solid #cecece'
          }
        }else{
          this.hint_username=''
          this.$refs.log_username.style.border='0.0625rem solid #cecece'
        }
      },
      checkPswLength(){
        if(this.password){
          let length=this.password.length
          if(length>16){
            this.hint_password='密码过长'
            this.$refs.log_password.style.border='0.0625rem solid #ff0000'
          }else if(length<7){
            this.hint_password = '密码过短'
            this.$refs.log_password.style.border = '0.0625rem solid #ff0000'
          }else{
            this.$refs.log_password.style.border='0.0625rem solid #cecece'
            this.hint_password=''
          }
        }

      },
      //简单加密
      changePassword(str){
        str=[...str]
        let length=Math.floor(str.length/3)
        for(let i=1;i<=length;i++){
          str.splice(i*3,0,'//')
        }
        return str.join("")
      },
      clickCheckbox(){
        this.hint_agree=''
      },
      goToZcsm(){
        const {href}=this.$router.resolve({
          name:'zcsm',
        })
        window.open( href ,'_blank')
      }
    }
  }
</script>

<style scoped>
  .home-page-body {
  }

  .home-page {
    width: 96rem;
    height: 49rem;
    background: #e4f2f5;
    box-shadow: 0 0 30px 6px rgba(40, 40, 40, 0.2);
    margin: 4rem auto 0;
  }
  @media screen and (max-width: 1080px){
    .home-page{
      margin: auto;
      width: 36.8rem;
    }
    .user-window{

    }
  }

  .home-page:after {
    content: ".";
    display: block;
    height: 0;
    clear: both;
    visibility: hidden;
  }

  .cover-photo {
    max-width: calc(100% - 31.25rem);
    width: 59.2rem;
    height: 100%;
    float: left;
    background: #eee;
    background: url(../assets/cover.jpg);
    background-size: cover;
    background-repeat: no-repeat;
    background-position: center;
  }
    @media (max-width: 1080px) {
      .cover-photo{
        display: none;
      }
    }
  .user-option{
   margin-bottom: 3rem;
    height: 2rem;
  }

  .user-window {
    width: 36.8rem;
    height: 100%;
    float: left;
    background: #f7fafb;
    padding: 3rem 7rem;
  }

  a, a:link, a:active, a:visited {
    font-size: 1.5rem;
    text-decoration: none;
    color: black;
    cursor: pointer;
  }

  .user-input, .input-area {
    width: 100%;
  }
  .login-input,.forget-input{
    margin-top: 8rem;
  }
  .forget-input{}

  .input-area {
    height: 4rem;
    text-indent: 1.5rem;
    font-size: 1.3rem;
    color: #9b9b9b;
    border: 0.0625rem solid #cecece;
  }

  .a-active, .a-not-active {
    padding-right: 0.5rem;
    float: left;
  }

  .a-active {
    color: #4a4a4a !important;
  }

  .a-not-active {
    color: #9b9b9b !important;
  }

  .border-a {
    padding-left: 0.5rem;
    border-left: 0.0625rem solid #9b9b9b;
  }

  .checkbox label {
    font-size: 1rem;
    line-height: 1.25rem;
    color: #4a4a4a;
    float: left;
  }

  .checkbox a {
    font-size: 1rem;
    line-height: 1.25rem;
  }
  .a-zcsm{
    color:#4a4a4a;
    float: left;
  }
  .checkbox a:hover{
    color: #9ad3e2;
  }

  .return-to-another {
    float:right;
    color: #9ad3e2;
  }

  .to-do-box {
    width: 100%;
    height: 3.25rem;
    margin-top: 3rem;
  }

  .to-do-btn {
    height: 100%;
    width: 100%;
    font-size: 1.2rem;
    padding: 0 4rem !important;
    line-height: 3.25rem;
    border-radius: 3.25rem;
    background: #9ad3e2;
    color: white;
    font-weight:600;
  }
  .to-do-btn:hover{
    cursor: pointer;
    background: #2cbec6;
  }
  .register-box {
    margin-top: 0;
  }

  .yzm-box {
    position: relative;
    display: flex;
    justify-content: space-between;
    align-items: center;
  }

  .copyright {
    text-align: center;
    font-size: 1rem;
    color: #4a4a4a;
    position: fixed;
    bottom: 1vh;
    width: 100%;
  }

  /*checkbox样式*/

  [type="checkbox"]:checked,
  [type="checkbox"]:not(:checked)
  {
    position: absolute;
    left:-999999px;
    opacity: 0;
  }
  [type="checkbox"]:checked + label,
  [type="checkbox"]:not(:checked) + label
  {
    position: relative;
    padding-left: 1.75rem;
    cursor: pointer;
    line-height: 1.25rem;
    display: inline-block;
    color: #666;
  }
  [type="checkbox"]:checked + label:before,
  [type="checkbox"]:not(:checked) + label:before
  {
    content: '';
    position: absolute;
    left: 0;
    top: 0;
    width: 1.125rem;
    height: 1.125rem;
    border: 0.0625rem solid #ddd;
    background: #fff;
  }
  [type="checkbox"]:checked + label:after,
  [type="checkbox"]:not(:checked) + label:after
  {
    content: '';
    width: 0.5rem;
    height: 0.5rem;
    background: #00a69c;
    position: absolute;
    top: 0.375rem;
    left: 0.375rem;
    -webkit-transition: all 0.2s ease;
    -moz-transition: all 0.2s ease;
    -o-transition: all 0.2s ease;
    transition: all 0.2s ease;
  }
  [type="checkbox"]:not(:checked) + label:after
  {
    opacity: 0;
    -webkit-transform: scale(0);
    -moz-transform: scale(0);
    -o-transform: scale(0);
    -ms-transform: scale(0);
    transform: scale(0);
  }
  [type="checkbox"]:checked + label:after
  {
    opacity: 1;
    -webkit-transform: scale(1);
    -moz-transform: scale(1);
    -o-transform: scale(1);
    -ms-transform: scale(1);
    transform: scale(1);
  }
</style>
