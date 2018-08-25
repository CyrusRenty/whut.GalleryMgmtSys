<template>
    <div class="sign">
      <div class="bread-list"><span @click="getBack" class="get-back">返回个人主页</span><span> - 签约</span></div>
      <div class="nav">
        <div v-for="(item,index) in nav_list" @click="changeStatus(index)" :class="{active:index<=current_show}" class="nav-item">
          <span class="item-num" :class="{active_item:index<=max_show}"><span v-if="index>=max_show">{{index+1}}</span><span class="complete-bg" v-else></span></span>
          <span class="item-text" :class="{active_item_text:index<=max_show}">{{item.text}}</span>
        </div>
      </div>
      <div class="content">
        <div v-if="nav_list[0].show">
          <pre class="pre1">
            <h2>签约摄影师协议</h2>
    <pre class="contract">
一、签约摄影师与乙方合作的概要
签约摄影师向乙方提供其拥有自主版权的摄影作品以及相关文字信息，并授权乙方在本协议规定的范围内进行图片使用权的代理，乙方为此向签约摄影师提供包括网络服务、数字图像技术服务、信息整合服务等综合的代理服务体系。

二、签约摄影师就其自主版权图片作品向乙方授权的许可范围和保证义务
1、签约摄影师对其自主版权的图片均在下属范围内授权乙方享有完全的权利：
授权乙方代理，同时乙方也接受该项授权，作为其自主版权的图片在武汉理工大学的使用权代理。乙方因此拥有签约摄影师授权图片使用权的代理权，但是该图片的其他附属权利（包括版权）仍为签约摄影师所有。
2、签约摄影师就其自主版权的图片作品授权乙方进行使用权代理。在合法范围内，乙方无需就每一次图片使用权的代理征询签约摄影师的意见，签约摄影师也不能因为用途原因而限制乙方的代理权限。
3、签约摄影师对其授权图片须履行如下保证义务：
保证授权乙方的图片为其专有版权的图片（原图），包括已方每期的场景的规定，如果授权图片为与他人共享著作权的图片，必须向乙方明确提示。
保证授权乙方对其授权图片的一切合法使用，包括乙方授权客户的有偿使用，在本协议期间，须保证不发生任何阻碍乙方行使该权利的留置权或其它妨碍。
保证授权乙方的图片和文字不涉及任何侵权事宜，不对任何民事主体造成诽谤、侵害隐私权，不触犯任何第三方的版权或商标权。
保证授权乙方的图片和文字不违背中华人民共和国的相关法律法规、不违背国际法的相关准则。
4、签约摄影师因违反上述义务规定，给第三方或乙方造成损失，乙方有权根据有关事实申请仲裁。乙方因超出签约摄影师上述授权范围对签约摄影师造成损失，签约摄影师有权提出相应仲裁申请。

三、乙方的义务
乙方向签约摄影师提供包括网络服务、数字图像技术服务、信息整合服务等综合的代理服务体系。

四、签约摄影师的权益保障
对于乙方的图片用户或者其他第三者因不当使用签约摄影师的图片、未经授权擅自使用签约摄影师的图片以及其他侵犯签约摄影师图片的知识产权的情形，签约摄影师可以自行解决侵权事宜，也可以全权委托乙方通过协商或法律途径进行解决，在后一种选择下，签约摄影师须与乙方进行相关书面约定。

五、免责事项
在下列情形下致使双方不能履行或不能完全履行本协议，双方互不承担责任：
不可抗力；
双方协议提前终止本协议；
其他符合免除责任的情形。

六、其他事项
此协议为有限的协议，双方的权利义务以此协议为唯一合法陈述。
本协议的双方当事人如因执行本协议发生争执，均可协商解决，如协商无法解决，任何一方有权向共青团武汉理工大学委员会仲裁委员会申请仲裁，该仲裁委员会就相关争议做出的仲裁为终局仲裁，对双方均有法定约束力。

</pre>
          </pre>
          <input type="button" value="同意合同" class="sign-submit" @click="agreeContract"/>
        </div>
        <div v-else-if="nav_list[1].show">
          <div class="user-form">
            <div class="content-warp">
              <div class="left-wrap">
                <div class="left">
                  <div class="wrap" v-if="!ID_card_image">
                    <i @click="fileChoice"></i>
                    <div>上传身份证（反面）</div>
                  </div>
                  <img v-if="ID_card_image" :src="ID_card_image.src" @click="fileChoice"/>
                  <input type="file" accept="image/*" @change="setImage" ref="ID_card"/>
              </div>
                <div class="hint">{{hint_ID_card}}</div>
            </div>
            <div class="right">
              <div class="form-item"><span>姓名</span><input title="姓名" type="text" v-model="name" ref="sign_name"/></div>
              <div class="hint">{{hint_name}}</div>
              <div class="form-item"><span>专业班级</span><input title="专业班级" type="text" v-model="zybj" ref="sign_class"/></div>
              <div class="hint">{{hint_class}}</div>
              <div class="form-item"><span>电话号码</span><input title="电话号码" type="number" min="0" max="9" v-model="tel" ref="sign_tel" @blur="blurTel"/></div>
              <div class="hint">{{hint_tel}}</div>
              <div class="form-item"><span>QQ</span><input title="QQ" type="number" min="0" max="9" v-model="QQ" ref="sign_QQ" @blur="blurQQ"/></div>
              <div class="hint">{{hint_QQ}}</div>
            </div>
            </div>
            <div class="btn-wrap"><input type="button" value="提交" @click="submit" class="sign-submit"/></div>
          </div>
        </div>
        <div v-else-if="nav_list[2].show">
          <div v-if="this.max_show!==3">
            <img src="../../../assets/Waiting.png" class="img-wait">
            <h2>正在审核</h2>
            <div class="remind">审核需要1-2天时间，请耐心等待</div>
          </div>
         <div v-if="this.max_show===3">
           <img src="../../../assets/Success.png" class="img-wait">
           <h2>申请签约成功</h2>
           <div class="remind">恭喜你已经获得签约摄影师权限，祝合作愉快！</div>
         </div>
        </div>
        <div v-else-if="nav_list[3].show">
          <img src="../../../assets/Success.png" class="img-wait">
          <h2>申请签约成功</h2>
          <div class="remind">恭喜你已经获得签约摄影师权限，祝合作愉快！</div>
          <input type="button" value="回到个人主页" class="sign-submit" @click="getBack"/>
        </div>
      </div>
    </div>
</template>

<script>
  import {sendAgree,sendUserInfo,getSignStatus} from "../../../api/action";
  export default {
        name: "sign",
      data(){
          return {
            name:'',
            zybj:'',
            tel:'',
            QQ:'',
            ID_card_image:'',
            nav_list:[
              {text:'合同信息',show:true,pass:true},
              {text:'提交申请',show:false,pass:false},
              {text:'审核结果',show:false,pass:false},
              {text:'正式签约',show:false,pass:false}],
            current_show:0,
            max_show:0,
            id:0,
            hint_name:'',
            hint_class:'',
            hint_tel:'',
            hint_QQ:'',
            hint_ID_card:''
          }
      },
      methods:{
        changeStatus(index){
          for(let i=0;i<this.current_show+1;i++){
            this.nav_list[i].pass=true
          }
          if(this.nav_list[index].pass){
            this.nav_list[this.current_show].show=false;
            this.nav_list[index].show=true;
            this.current_show=index
          }
        },
        agreeContract(){
          this.nav_list[0].show=false;
          this.nav_list[1].show=true;
          this.current_show=1
          this.setMaxShow()
          let data=new FormData()
          data.append('user',this.$store.state.user.userInfo.id)
          sendAgree(data).then((res)=>{
            console.log(res)
          }).catch((res)=>{
            console.log(res)
          })
        },
        submit(){
          if(!this.ID_card_image){
            this.hint_ID_card='请上传您的身份证反面图片'
            setTimeout(()=>{
              this.hint_ID_card=''
            },1800)
            return
          }
          if(!this.name){
            this.hint_name='请输入姓名'
            this.$refs.sign_name.style.border="0.0625rem solid #ff0000"
            setTimeout(()=>{
              this.hint_name=''
              this.$refs.sign_name.style.border="0.0625rem solid #cecece"
            },2000)
            return
          }
          if(!this.zybj){
            this.hint_zybj='请输入你的专业班级'
            this.$refs.sign_class.style.border="0.0625rem solid #ff0000"
            setTimeout(()=>{
              this.hint_zybj=''
              this.$refs.sign_class.style.border="0.0625rem solid #cecece"
            },2000)
            return
          }
          if(this.hint_tel||!this.tel){
            this.hint_tel='请输入正确电话号码';
            this.$refs.sign_tel.style.border="0.0625rem solid #ff0000";
            setTimeout(()=>{
              this.hint_tel='';
              this.$refs.sign_tel.style.border="0.0625rem solid #cecece"
            },2000)
            return
          }
          if(!this.QQ||this.hint_QQ){
            this.hint_QQ='请输入正确QQ';
            this.$refs.sign_QQ.style.border="0.0625rem solid #ff0000";
            setTimeout(()=>{
              this.hint_QQ='';
              this.$refs.sign_QQ.style.border="0.0625rem solid #cecece"
            },2000)
            return
          }
          this.nav_list[1].show=false;
          this.nav_list[2].show=true;
          this.current_show=2
          this.setMaxShow()
          let data=new FormData()
          data.append('name',this.name)
          data.append('p_class',this.zybj)
          data.append('mobile',this.tel)
          data.append('qq',this.QQ)
          data.append('id_card',this.ID_card_image.file)
          data.append('status','2')
          console.log(data)
          sendUserInfo(this.id,data).then((res)=>{
            console.log(res)
          }).catch((res)=>{
            console.log(res)
          })
        },
        setMaxShow(){
          if(this.current_show>this.max_show)
            this.max_show=this.current_show
        },
        setImage(){
          let ID_card=this.$refs.ID_card.files[0]
          console.log(ID_card)
          const item={
            name:ID_card.name,
            size:ID_card.size,
            file:ID_card,
          }
          this.html5Reader(ID_card,item)
          this.ID_card_image=item;
        },
        html5Reader(file, item){
          const reader = new FileReader();
          reader.onload = (e) => {
            this.$set(item, 'src', e.target.result)
          };
          reader.readAsDataURL(file)
        },
        fileChoice(){
          this.$refs.ID_card.click()
        },
        blurTel(){
          let str=this.tel
          if(str.length!==11){
            this.hint_tel='输入数字长度不合法'
          }else if(str.charAt(0)==="0"||parseFloat(str)!==parseInt(str)){
            this.hint_tel='输入格式错误'
          }else this.hint_tel=''
          if(!this.hint_tel)
            this.$refs.sign_tel.style.border='0.0625rem solid #cecece';
          else
          this.$refs.sign_tel.style.border='0.0625rem solid #ff0000';
        },
        blurQQ(){
          let str=this.QQ
          if(str.length>11||str.length<5){
            this.hint_QQ='输入数字长度不合法'
          }else if(str.charAt(0)==="0"||parseFloat(str)!==parseInt(str)){
            this.hint_QQ='输入格式错误'
          }else this.hint_QQ=''
          if(!this.hint_QQ)
            this.$refs.sign_QQ.style.border='0.0625rem solid #cecece';
          else
            this.$refs.sign_QQ.style.border='0.0625rem solid #ff0000';
        },
        getBack(){
          this.$store.commit('SET_SHOW_SIGN')
        },
        getStatus(){
          getSignStatus().then((res)=>{
            this.current_show=res.data.status
            this.max_show=res.data.status
            this.nav_list[0].show=false
            this.nav_list[this.max_show].show=true
            this.id=res.data.id
          })
        }
      },
      created(){
          this.getStatus()
      },
      computed:{

      }
    }
</script>

<style scoped>
  .margin-t{
    margin-top: 5rem;
  }
  .sign{
    z-index: 100;
    background:#f7fafb;
    padding: 2rem 15.25rem 5rem;
    font-size: 1.25rem;
  }
  .bread-list{
    float: left;
    margin-bottom: 0.5rem;
    height:2rem;
    color: #9b9b9b;
  }
  .get-back{
    font-size: 1.5rem;
    cursor: pointer;
    color: #4a4a4a;
  }
  .get-back:hover{
    color:#9ad3e2;
  }
  .nav{
    display: flex;
    background: #fff;
    width: 100%;
    height: 5rem;
    line-height: 50px;
  }
  .nav-item{
    width: 25%;
    height: 100%;
    align-items: center;
    justify-content: center;
    display: flex;
    color: #fff;
  }
  .item-num{
    background: #e9e9e9;
    display: flex;
    width: 2.5rem;
    height: 2.5rem;
    margin-right: 5px;
    align-items: center;
    justify-content: center;
    -webkit-border-radius: 50%;
    -moz-border-radius: 50%;
    border-radius: 50%;
    color: #fff;
  }
  .active_item{
    background: #9ad3e2;
  }
  .complete-bg{
    height: 50%;
    width: 65%;
    background:url(../../../assets/Complete.png) no-repeat center;
    -webkit-background-size: 100% 90%;
    background-size: 100% 90%;
  }
  .active{
    color: #9ad3e2!important;
    border-bottom: 0.125rem solid #9Ad3e2;
  }
  .item-text{
    color:#9b9b9b;
  }
  .active_item_text{
    color:#9ad3e2;
  }
  .content{
    background: #fff;
    min-height: 500px;
    padding: 4rem 7.75rem;
  }
  /*
  提交申请
   */
  .user-form{
    display: flex;
    justify-content: space-between;
    flex-direction: column;
    text-align: left;
    flex-wrap: nowrap;
    width: 100%;
  }
  .user-form .content-warp{
    display: flex;
    justify-content: space-between;
  }
  .user-form .left{
    width: 26.5rem;
    height: 22rem;
    background: #e4f2f5;
    display: flex;
    justify-content: center;
    align-items: center;
  }
  .user-form .left .wrap{
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
    color: #b9b9b9;
  }
  .user-form .left img{
    width: 100%;
  }
  .user-form .left i{
    background: url(../../../assets/Add.png);
    background-size: 100% 100%;
    height: 4.5rem;
    width: 4.5rem;
    cursor: pointer;
    margin-bottom: 0.5rem;
  }
  .user-form .left input{
    display: none;
  }
  .user-form .right input{
    width: 30.125rem;
    height: 4rem;
    border: 0.0625rem solid #cecece;
    margin-left: 5.375rem;
    font-size: 1.25rem;
    text-indent: .5rem;
  }
  .user-form .right input:focus{
    border-color: #9ad3e2;
  }
  .user-from .right span{
    font-size: 1.25rem;
    text-align: right;
  }
  .form-item{
    display: flex;
    justify-content: flex-end;
    flex-wrap: nowrap;
    align-items: center;
    font-weight: bold;
    position: relative;
    margin: 0.2rem 0;
  }
  .user-form .btn-wrap{
    display: flex;
    justify-content: center;
  }

  .sign-submit{
    margin-top: 1.2rem;
    margin-bottom: 3.75rem;
    width: 20rem;
    height: 3rem;
    border-radius: 3rem;
    background: #2cbec6;
    color: #fff;
    font-size: 1.25rem;
    font-weight: 600;
    cursor: pointer;
  }
  /*
  合同
   */
  pre {
    white-space: pre-wrap; /*css-3*/
    /*white-space: -moz-pre-wrap; !*Mozilla,since1999*!*/
    /*white-space: -pre-wrap; !*Opera4-6*!*/
    /*white-space: -o-pre-wrap; !*Opera7*!*/
    /*word-wrap: break-word; !*InternetExplorer5.5+*!*/
  }
  .pre1{
    margin: 0;
    border: 1px solid #bcbcbc;
  }
  .contract-wrap{

  }
  .contract{
    color: #606060;
    width: 100%;
    text-align: left;
    padding: 0 5rem;
    line-height: 2rem;
  }
  .btn-agree{
    width: 12rem;
    height: 4rem;
    background: #2cbec6;
    border-radius: 4rem;
    margin-bottom: 5rem;
    color: #fff;
    font-size: 25px;
    cursor: pointer;
  }


  .img-wait{
    width: 10rem;
    margin-top: 5rem ;
  }
  .remind{
    color: #cecece;
  }
</style>
