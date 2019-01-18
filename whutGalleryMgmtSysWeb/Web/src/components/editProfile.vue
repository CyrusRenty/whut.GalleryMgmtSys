<template>
  <div class="editBox" v-if="show_edit">
    <!--<i class="deletePage" @click="cancel"></i>-->
  <div id="editProfile" class="clear" ref="editpf"  :style="styleObject">
    <div id="user-image">
      <vue-avatar :scale="scale" ref="vueavatar" @image-ready="onImageReady"/>
      <br>
      <label><input type="range" min=1 max=3 step=0.02 v-model="scale"/></label>
    </div>
    <div class="edit-warp">
      <div class="edit-item">
        <div class="short-width">
        <span class="font-middle font-MB">用户名</span>
        <input type="text" class="user-change-input " v-model="username" ref="change_username" @blur="checkNameExist" @input="inputUserName" title="昵称">
        <div class="hint">{{hint_username}}</div>
        </div>
        <div class="short-width">
          <span class="font-middle font-MB">QQ</span>
          <input type="text" class="user-change-input" maxlength="12" minlength="5" name="QQ" v-model="QQ" ref="change_QQ" title="QQ" @input="inputQQ">
          <div class="hint">{{hint_QQ}}</div>
        </div>

      </div>
      <div class="item-qq">
        <span class="font-middle font-MB">专业班级</span>
        <input type="text" class="user-change-input " v-model="zybj" ref="change_zybj"  @blur="cleanBorder" @input="inputZybj"  title="专业班级">

      </div>
      <div class="item-desc">
        <span class="font-middle font-MB">简介</span>
        <textarea title="简介" ref="change_desc" v-model="desc" maxlength="32"></textarea>
        <div class="hint">{{hint_desc}}</div>
      </div>

        <div class="sc-btn">
          <input type="button" class="submit" value="保存" @click="submit"/>
          <input type="button" class="cancel" value="返回" @click="cancel"/>
      </div>

    </div>

  </div>
    <hint ref="hint"/>
  </div>
</template>

<script>
    import VueAvatar from './VueAvatar'
    import {changeUserInfo, checkName} from "../api/user";
    import hint from './hint'

    export default {
        name: "editProfile",
        components:{VueAvatar,hint},
        data:function(){
            return{
              //插件数据
              rotation:0,
              scale: 1,
              username:'',
              zybj:'',
              desc:'',
              image:'',
              QQ:'',
              styleObject:{
                transition:'all 0.5s ease',
              },
              hint_username:'',
              hint_zybj:'',
              hint_desc:'',
              hint_QQ:'',
              hint_result:'',
              show_edit:false
          }
        },
        computed:{
        userInfo(){
          return this.$store.state.user.userInfo
        }
      },
        methods:{
          showEdit(){
            document.body.style.overflow='hidden';
            this.username=this.userInfo.username;
            this.QQ=this.userInfo.qq;
            this.desc=this.userInfo.desc;
            this.zybj=this.userInfo.p_class
            this.show_edit=true
          },
          cancel(){
            this.show_edit=false;
            document.body.style.overflow = 'auto';
          },
          submit(){
            this.image=this.$refs.vueavatar.getImageScaled();
            if(!this.username||this.hint_username){
              this.hint_username='请填写用户名';
              this.$refs.change_username.style.border='0.0625rem solid #ff0000';
              return
            }
            if(!this.checkQQ())
              return;
            let data=new FormData;
            if(this.image){
              data.append('image',this.image)
            }
              data.append('username',this.username);
              data.append('p_class',this.zybj);
              data.append('qq',this.QQ);
              data.append('desc',this.desc);
            changeUserInfo(this.userInfo.id,data).then((res)=>{
              if(res.data.id){
                this.$refs.hint.showHint('修改成功');
                this.reload()
                this.cancel()
              }
            }).catch((res)=>{
              console.log(res);
              this.$refs.hint.showHint('修改失败');
              this.reload()
            })
          },
          checkNameExist(){
            if(this.username!==this.$store.state.user.userInfo.username){
              checkName(this.username).then((res)=>{
                if(!res.data.msg){
                  this.hint_username='该用户名已存在';
                  this.$refs.change_username.style.border='0.0625rem solid #ff0000'
                }else{
                  this.hint_username='';
                  this.$refs.change_username.style.border='0.0625rem solid #cecece'
                }
              })
            }
          },
          inputUserName(){
            if(this.username.length>=6){
              let length=0;
              for(var i=0;i<this.username.length;i++){
                var a=this.username.charAt(i);
                if (a.match(/[^\x00-\xff]/ig) != null){
                  length+=2
                }else length+=1
              }
              if(length>12){
                this.hint_username='用户名过长';
                this.$refs.change_username.style.border='#ff0000 0.0625rem solid'
              }else{
                this.hint_username='';
                this.$refs.change_username.style.border='0.0625rem solid #cecece'
              }
            }else{
              this.hint_username='';
              this.$refs.change_username.style.border='0.0625rem solid #cecece'
            }
          },
          inputZybj(){
            this.hint_zybj='';
            this.$refs.change_zybj.style.border='0.0625rem solid #9ad3e2'
          },
          inputQQ(){
            this.hint_QQ='';
            this.$refs.change_QQ.style.border='0.0625rem solid #9ad3e2'
          },
          inputDesc(){
            if(this.desc.length>20){
              let length=0;
              for(var i=0;i<this.desc.length;i++){
                var a=this.desc.charAt(i);
                if (a.match(/[^\x00-\xff]/ig) != null){
                  length+=2
                }else length+=1
              }
              if(length>21){
                this.desc=this.desc.substring(0,21)
                this.hint_desc='简介过长'
                this.$refs.change_desc.style.border='#ff0000 0.0625rem solid'
              }
            }else{
              this.hint_desc=''
              this.$refs.change_desc.style.border='0.0625rem solid #9ad3e2'
            }
            if(this.desc.length===0){
              this.$refs.change_desc.style.border='0.0625rem solid #cecece'
            }
          },
          cleanBorder(){
            this.$refs.change_password.style.border='0.0625rem solid #cecece'
          },
          checkQQ(){
            let qq_length=this.QQ.length;
            if(qq_length>12||qq_length<9&&qq_length>0){
              this.hint_QQ='请填写正确QQ';
              this.$refs.change_QQ.style.border='0.0625rem solid #ff0000';
              return false
            }else{
              this.hint_QQ='';
              this.$refs.change_QQ.style.border='0.0625rem solid #cecece'
              return true
            }
          },
          reload(){
            this.$store.dispatch('GetUserInfo')
          },
          onImageReady () {
            this.scale =1;
          }
        },
    }
</script>

<style scoped>

/*样式css*/

.editBox{
  width: 100%;
  height: 100%;
  background-color: rgba(0,0,0,0.6);
  position: fixed;
  top: 0;
  left: 0;
  z-index: 100;
}
.deletePage{
  position: fixed;
  top: 5rem;
  right:25rem;
  height: 2rem;
  width: 2rem;
  background: url(../assets/delete.png);
  background-size:cover;
  cursor: pointer;
}
.user-change-input{
  width: 100%;
  height:2.8rem;
  background-color: #fff;
  text-indent: 1rem;
  font-size: 1.2rem;
  border:0.0625rem solid #cecece;
}
.short-width{
  width: 47%;
  display: inline-block;
  margin-bottom: 0.4rem;
}
#editProfile{
  margin: 5rem auto 0;
  background: #f7fafb;
  width: 58.5rem;
  height: 38rem;
  transition: all 1s;
  -moz-transition: all 1s;
  -webkit-transition: all 1s;
  -o-transition:all 1s;
}
#user-image{
  width: 21.625rem;
  height: 100%;
  float: left;
  background-color: #e4f3f6;
  position: relative;
}
.edit-warp{
  width: 36.875rem;
  height: 100%;
  float: left;
  text-align: left;
  padding:  2.75rem 2.625rem;
  background: #f7fafb;
}
.edit-warp span {
  text-align: left;
  margin-bottom: 1rem;
  display: inline-block;
}
.edit-item{
  width: 100%;
  display: flex;
  justify-content: space-between;
}
.item-qq{
  width: 100%;
  margin-bottom: 0.4rem;
}
.item-desc{
  width: 100%;
}
.item-desc textarea{
  height: 9rem;
  width: 100%;
  resize: none;
  outline: none;
  text-indent: 0.5rem;
  font-size: 1.2rem;
  border: 0.0625rem solid #cecece;
}
.item-desc textarea:focus{
  border: 0.0625rem solid #9ad3e2;
}
.sc-btn{
  width: 100%;
}
.sc-btn input{
  float: right;
}
.save-image div{
  text-align: center;
}
  input[type='text']:focus{
    border:0.0625rem solid #b5dee9;
  }
  /*
  range
   */
input[type=range] {
  -webkit-appearance: none;
  width: 10rem;
  border-radius: 0.625rem; /*这个属性设置使填充进度条时的图形为圆角*/
}
input[type=range]::-webkit-slider-thumb {
  -webkit-appearance: none;
}
input[type=range]::-webkit-slider-runnable-track {
  height: 0.7rem;
  border-radius: 0.625rem; /*将轨道设为圆角的*/
  box-shadow: 0 0.06rem 0.06rem #def3f8, inset 0 .1rem .1rem #0d1112; /*轨道内置阴影效果*/
}
input[type=range]{
  outline: none;
}
input[type=range]::-webkit-slider-thumb {
  -webkit-appearance: none;
  height: 1rem;
  width: 1rem;
  margin-top: -0.3125rem; /*使滑块超出轨道部分的偏移量相等*/
  background: #ffffff;
  border-radius: 50%; /*外观设置为圆形*/
  border: solid 0.125rem rgba(205, 224, 230, 0.5); /*设置边框*/
  box-shadow: 0 .125rem .125rem #3b4547; /*添加底部阴影*/
  cursor: pointer;
}
</style>
