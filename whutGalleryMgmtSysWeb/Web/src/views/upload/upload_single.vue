<template>
    <div class="upload-single" v-if="show_upload_pre">
      <div class="upload-s-box">
        <div class="head">
          <h2>上传预览图</h2>
          <span @click="closePage">×</span>
        </div>
        <div class="clear">
          <div class="left">
            <div class="image">
              <div class="before-img" v-if="status==='ready'">
                <i @click="choiceFile"></i>
                <span>上传图片</span>
                <span>支持JPG、PNG，大小不超过5M</span>
                <span>建议尺寸800*600</span>
              </div>
              <div class="canvas-wrap" v-show="status==='done'" >
              <vue-avatar ref="canvas" @getFile="getFile" :scale="scale" :rotation="rotate" @setStatus="setStatus"/>
              </div>
          </div>
          <div class="left-btm">
            <span @click="choiceFile">重新上传</span>
            <div>
              <img src="../../assets/icon/rotate.png" @click="changeRotate"/>
              <img src="../../assets/icon/decrease.png" @click="decrease"/>
              <img src="../../assets/icon/increase.png" @click="increase"/>
            </div>
          </div>
          </div>
          <div class="right">
            <img :src="src" class="right-img" v-if="this.src">
            <div class="info-wrap">
            <div>
              <div class="img-name">图片名称</div>
              <div>图片分类</div>
            </div>
            <div class="bottom-wrap">
              <img :src="$store.state.user.userInfo.image" class="right-user-img">
              <span>{{this.$store.state.user.userInfo.username}}</span>
            </div>
            </div>
          </div>
          <div class="sc-btn">
            <input class="cancel" value="取消" type="button" @click="closePage"/>
            <input class="submit" value="确认" type="button" @click="submit"/>
          </div>
        </div>
      </div>
      <hint ref="hint"/>
      <!--<input type="file" accept="image/*" style="display: none;" @change="fileChanged" ref="file">-->
    </div>
</template>

<script>
  import VueAvatar from './VueAvatar'
  import hint from '../../components/hint'
    export default {
        name: "upload_single",
      components:{
        VueAvatar,
        hint
      },
      data(){
          return {
            show_upload_pre:false,
            status:'ready',
            src:'',
            scale:1,
            rotate:0,
            file:{}
          }
      },
      methods:{
          showUploadPre(){
            this.show_upload_pre=!this.show_upload_pre
          },
        closePage(){
          this.status='ready';
          this.src='';
          this.show_upload_pre=!this.show_upload_pre;
          document.documentElement.style.overflow='auto'
        },
        choiceFile(){
          // this.status="done";
          this.$refs.canvas.clicked()
        },
        html5Reader(file, item){
          const reader = new FileReader();
          reader.onload = (e) => {
            this.$set(item, 'src', e.target.result)
          };
          reader.readAsDataURL(file)
        },
        getFile(file){
            if(this.status==='done'){
              this.file=file;
              const reader = new FileReader();
              reader.onload = (e) => {
                this.src=e.target.result
              };
              reader.readAsDataURL(file)
            }
        },
        submit(){
          this.$emit('getFile',this.file)
          this.closePage()
        },
        decrease(){
          if(this.scale-0.1>0.1)
          this.scale=this.scale-0.1
        },
        increase(){
            if(this.scale<5)
          this.scale=this.scale+0.1
        },
        changeRotate(){
          this.rotate=this.rotate+90
        },
        setStatus(status){
            if(!status){
              this.$refs.hint.showHint(" 请上传像素大于400×300的图片")
            }else this.status='done'
        }
      }
    }
</script>

<style lang="scss" scoped>
  @import "../../styles/variables";
  .upload-single{
    position: fixed;
    display: flex;
    justify-content: center;
    align-items: center;
    top: 0;
    left: 0;
    z-index:3;
    background: rgba(0,0,0,.4);
    width: 100%;
    height: 100%;
  }
  .upload-s-box{
    position: fixed;
    width: 61.625rem;
    height: 38.9rem;
    padding: 0 3rem;
    background: #fff;
    .head{
      display: flex;
      justify-content: space-between;
      margin: 1.5rem 0;
      text-align: left;
    }
    .left,.right{
      float: left;
    }
  }
  .head{
    h2{
      display: inline-block;
      margin: 0;
    }
    span{
      line-height: 2rem;
      font-size: 3rem;
      cursor: pointer;
    }
  }
  .left{
    .image{
      display: flex;
      justify-content: center;
      align-items: center;
      width: 33.3rem;
      height: 25rem;
      background: $bg;
      .before-img{
        display: flex;
        justify-content: center;
        align-items: center;
        flex-direction: column;
        font-size: 1rem;
        color: $f-light;
        i{
          display: inline-block;
          width: 4.6875rem;
          height: 4.6875rem;
          background: url(../../assets/big_icon/add.png) no-repeat center;
          -webkit-background-size: cover;
          background-size: cover;
          cursor: pointer;
        }
        span:nth-child(2){
          margin: .75rem 0;
          font-size: 1.125rem;
          color: $f-deep;
        }
      }
    }
  }
  .left-btm{
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin: .75rem 0 1.5rem 0;
    span{
      color: $normal;
      cursor: pointer;
    }
    img{
      width: 1.125rem;
      height: 1.125rem;
      margin-left: 1.5rem;
    }
  }
  .canvas-wrap{
    width: 100%;
    height: 100%;
    display: flex;
    justify-content: center;
    align-items: center;
    background: url(../../assets/canvas_bg.svg);
  }
  .right{
    display: flex;
    flex-direction: column;
    justify-content: flex-end;
    width: 19.1875rem;
    height: 25rem;
    margin-left: 1.5rem;
    text-align: left;
    background: #e9e9e9;
    box-shadow: 0 0 1px #9b9b9b;
  }
  .right-img{
    height: 14.48rem;
    width: 19.1875rem;
  }
  .info-wrap{
    padding:  0 1rem;
    background: #fefefe;
  }
  .img-name{
    margin: 1.5rem 0 .5rem 0;
    font-size: 1.25rem;
    font-weight: 600;
    &:after{
      display: block;
      content: '';
      width: 2rem;
      height: .1rem;
      margin-top: .5rem;
      background: $normal;
    }
  }
  .bottom-wrap{
    margin: .7rem 0;
    padding-top: 0.5rem;
    border-top: 0.0625rem solid #e9e9e9;
    display: flex;
    justify-content: flex-start;
    align-items: center;
  }
  .right-user-img{
    border-radius: 50%;
    width: 3rem;
    height: 3rem;
  }
  .sc-btn{
    float: left;
  }
</style>
