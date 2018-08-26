<template>
  <div>
  <div class="declareHead" ref="zcsm_header">
    <div class="head-left">
      <div class="logo"><a href="http://111.231.230.54/tslg/main"></a> </div><span class="head-line"></span><span class="zcsm-title">{{title}}</span>
    </div>
    <div class="headLink">
      <a @click="goLogin">登录</a>
      <a class="borderSpan" @click="goRegister">注册</a>
    </div>
  </div>
  <div class="declareDetail clear">
    <div class="content-left">
      <a :class="{a_active:true}">注册声明</a>
    </div>
    <div class="content-right">
    <h2 class="registerTitle">注册声明</h2>
    <p>
    <h2>1.提示条款</h2>
    <p class="nowrap">各条款标题仅为帮助您理解该条款表达的主旨之用，不影响或限制本协议条款的含义或解释。为维护您自身权益，建议您仔细阅读各条款具体表述。</p>
    <p class="nowrap">您在申请注册流程中点击同意本协议之前，应当认真阅读本协议。请您务必审慎阅读、充分理解各条款内容，特别是免除或者限制责任的条款、法律适用和争议解决条款。免除或者限制责任的条款将以粗体下划线标识，您应重点阅读。如您对协议有任何疑问，可向千图网客服咨询。</p>
    <p class="nowrap">
      当您按照注册页面提示填写信息、阅读并同意本协议且完成全部注册程序后，即表示您已充分阅读、理解并接受本协议的全部内容，并与千图网达成一致，成为千图网网站“用户”。 阅读本协议的过程中，如果您不同意本协议或其中任何条款约定，您应立即停止注册程序。如果您未申请注册流程，或者在本协议生效前已成为千图网的注册用户，则您通过访问和/或使用千图网，即视为您表示同意接受本协议的全部内容，否则请您不要访问或使用千图网平台网站。
    </p>
    </p>
    <p>
    <h2>2. 协议范围</h2>
    <h3>2.1 签约主体</h3>
    <p class="nowrap">本协议由您与千图网经营者（上海千图网络科技有限公司）共同缔结，本协议对您与千图网经营者均具有合同效力。</p>
    <p class="nowrap">本协议项下，千图网经营者可能根据千图网的业务调整而发生变更，变更后的千图网经营者与您共同履行本协议并向您提供服务，千图网经营者的变更不会影响您本协议项下的权益。</p>
    <h3>2.2补充协议</h3>
    由于互联网行业高速发展，您与千图网签署的本协议列明的条款并不能完整罗列并覆盖您与千图网所有权利与义务，现有的约定也不能保证完全符合未来发展的需求。因此， 千图网公示的相关声明及政策、千图网相关的规则和协议均为本协议的补充协议，与本协议不可分割且具有同等法律效力。如您使用千图网服务，视为您同意上述补充协议。
    <p>
    </p>
    <h2>3.帐号注册与使用</h2>
    <h3>3.1用户资格</h3>
    您确认，在您开始注册程序使用千图网服务前，您应当具备中华人民共和国法律规定的与您行为相适应的民事行为能力。若您不具备前述与您行为相适应的民事行为能力，则您及您的监护人应依照法律规定承担因此而导致的一切后果。
    <h3>3.2 帐号说明</h3>
    <p class="nowrap">【帐号获得】当您按照注册页面提示填写信息、阅读并同意本协议且完成全部注册程序后，您可获得千图网帐号并成为千图网用户。</p>
    <p class="nowrap">【帐号使用】您有权使用您绑定千图网帐号的手机号进行手机号验证码登录、使用您绑定千图网帐号的QQ、微信、微博进行第三方授权登录千图网。由于您的千图网帐号关联您的个人信息及千图网商业信息，您的千图网帐号仅限您本人使用。未经千图网同意，您不得直接或间接授权第三方使用您千图网帐号或获取您帐号信息。因未经千图网同意的授权行给千图网造成的所有损失由您赔偿，千图网有权冻结您的帐号，并不予退还未使用的VIP权限。如千图网判断您帐号的使用可能危及您的帐号安全及/或千图网信息安全的，千图网可拒绝提供相应服务或终止本协议。</p>
    <p class="nowrap">【帐号转让】由于用户帐号关联用户信用信息，仅当有法律明文规定、司法裁定或经千图网同意，并符合千图网规则规定的用户帐号转让流程的情况下，您可进行帐号的转让。您的帐号一经转让，该帐号项下权利义务一并转移。除此外不得以任何方式转让、赠与、外借、出租或售卖您的千图网帐号，否则千图网有权追究您的违约责任，且由此产生的一切责任均由您承担。</p>
    <p class="nowrap">【实名认证】作为千图网经营者，为使您更好地使用千图网的各项服务，保障您的帐号安全，千图网可要求您按千图网要求及我国法律规定完成实名认证。</p>
    <p class="nowrap">【帐号回收】如您的帐号长期未登录，千图网有权予以进行注销等清理，您的帐号将不能再登录千图网，相应服务同时终止。千图网在对此类帐号进行清理前，将以包括但不限于网站公告、站内消息等方式通知您。</p>
    <p class="nowrap">【帐号下载限制】千图网赋予每个帐号在满足一定条件的情况下，通过网站正式程序下载作品的资格，但作为网站管理者，有权为保护帐号安全以及网站运营规则，同时给予一定的下载限制（如1秒钟下载超过5次、1天内下载超过100次等高频、大量下载行为进行暂时限制下载），而不因此承担法律责任。千图网向用户提供申诉途径，但千图网有权根据该使用者的具体情况，自主决定是否开放下载限制。</p>
    </p>
    </div>
  </div>
    <div class="copyright">
      Copyright©&nbsp;&nbsp;&nbsp;2018&nbsp;&nbsp;&nbsp;共青团武汉理工大学委员会宣传部
    </div>
  </div>
</template>

<script>
    import {goRegister} from "../utils/user";

    export default {
        name: "zcsm",
      data(){
          return {
            title:'注册声明',
            head_style:{
              position:'fixed',
              top:'0',
            }
          }
      },
      mounted(){
        window.addEventListener('scroll',this.setHead)
      },
      destroyed(){
          window.removeEventListener('scroll',this.setHead)
      },
      methods:{
        goLogin(){
          this.$router.push({name:'login'})
        },
        goRegister(){
         goRegister()
        },
        setHead(){
          if(document.documentElement.scrollTop>80){
            this.$refs.zcsm_header.style.position='fixed'
            this.$refs.zcsm_header.style.top=0
          }else{
            this.$refs.zcsm_header.style.position='relative'
          }
        }
      }
    }
</script>

<style scoped>
  /*声明页面的头部样式*/
  .declareHead{
    height:5rem;
    padding:0 10rem;
    display:flex;
    justify-content:space-between;
    border-bottom: 0.0625rem solid #cecece;
    align-items: center;
    width: 100%;
    background: #fff;
  }
  .head-left{
    display: flex;
    align-items: center;
  }
  .logo,.headLink{
    display:inline-block;
  }
  .zcsm-title{
    height: 100%;
    font-size: 1.5rem;
    line-height: 5rem;
  }
   .head-line{
    width: .13rem;
    display: inline-block;
    height: 2rem;
    margin: 1rem 1rem;
    background: #4a4a4a;
  }
  .logo{
    display: inline-block;
    float: left;
    height: 1.875rem;
    width: 6.3125rem;
    background: url(../assets/header_logo.png) center;
    background-size:100% 100%;
    cursor: pointer;
  }
  .logo a{
    display: block;
    width: 100%;
    height: 100%;
  }
  .clear:after{
    content: '';
    display: block;
    clear: both;
    visibility: hidden;
    line-height: 0;
    height: 0;
    font-size: 0;
  }
  .headLink a{
    font-size:1.5rem;
    padding:0 0.5rem;
    cursor:pointer;
  }
  .headLink a.borderSpan{
    border-left:0.0625rem solid #000;
  }

  /*声明页面的声明内容样式*/
  .declareDetail{
    text-align: left;
    background-color: #fff;
    width:100rem;
    line-height: 2rem;
    font-size: 1.1rem;
    margin:3rem auto 5rem;
  }
  .declareDetail h2,h3{

  }
  .declareDetail h2{
    font-size: 1.4rem;
  }
  .declareDetail h3{
    font-size: 1.2rem;
  }
  .content-left{
    width: 10rem;
    float: left;
    height:100%;
    font-size:1.1rem;
  }
  .content-left a{
    cursor:pointer;
    padding-left: 2rem;
  }
  .a_active{
    color: #9ad3e2;
  }
  .content-right{
    float: left;
    width:90rem;
    background:#f7fafb;
    padding:2rem 2rem;
    font-size:1.1rem;
  }
  .registerTitle{
    display: inline-block;
    color: #9ad3e2;
    border-bottom: 5px solid #9ad3e2;
    font-size: 22px;
  }
  h2.registerTitle{
    font-weight: 700;
    padding-bottom: 16px;
    margin-bottom: 16px;
  }
  .declareDetail p{
    padding-bottom: 0px;
  }
  p.nowrap{
    font-size: 1.1rem;
    display: inline-block;
    margin: 0;
  }
  .copyright {
    height: 4rem;
    line-height: 4rem;
    text-align: center;
    font-size: 1rem;
    color: #4a4a4a;
    width: 100%;
   border-top: 0.0625rem solid #cecece;
  }

</style>
