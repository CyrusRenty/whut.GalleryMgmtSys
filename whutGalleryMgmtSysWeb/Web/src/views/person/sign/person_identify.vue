<template>
  <div class="editBox" v-if="show_identify" @click="hide">
    <div id="editProfile" ref="editpf" @click.stop="show">
      <div id="userimage-area">
        <input type="file" accept="image/*" @change="fileChanged" ref="file">
        <img :src="image.src" v-if="image" class="image-identify" @click="selectFile" >
        <span v-if="!image">
          <span class="center-text" @click="selectFile">+</span>
          <span class="user-material">提交材料截图</span>
        </span>
        <div class="hint">{{hint_image}}</div>
      </div>
      <div id="type-area">
        <p>{{status}}</p>
        <div class="typearea-line">
          <p>组织名称</p>
          <input class="input" type="text" v-model="name" ref="identify_name" @blur="cleanBorder">
          <div class="hint">{{hint_name}}</div>
        </div>
        <div class="typearea-line">
          <p>指导老师</p>
          <input class="input"  type="text" v-model="teacher" ref="identify_teacher">
          <div class="hint">{{hint_teacher}}</div>
        </div>
        <div class="typearea-line" id="typearea-btn">
          <div class="hint">{{hint_result}}</div>
          <input type="button" class="bottom confirm" value="提交" @click="submit"/>
          <input type="button" class="bottom cancel" value="取消" @click.stop="hide"/>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
    import {certification} from "../../../api/action";
    import {getCertification} from "../../../api/get";

    export default {
      name: "person_identify",
      data(){
        return{
          status:'未认证',
            image:'',
            show_identify:false,
            name:'',
            teacher:'',
          hint_image:'',
          hint_name:'',
          hint_teacher:'',
          hint_result:''
        }
      },
      created(){
        getCertification().then((res)=>{
          if(res.data.status===0)
            this.status='未认证'
          if(res.data.status===1)
            this.status='后台认证中'
          if(res.data.status===2)
            this.data.status='已认证'
        })
      },
      mounted(){

      },
      methods: {
        selectFile(){
          this.$refs.file.click()
          this.hint_image=''
        },
        hide() {
          document.body.style.overflow = 'auto';
          this.show_identify=false
          this.image=''
          this.name=''
          this.teacher=''
        },
        show(){
          document.body.style.overflow = 'hidden'
          this.show_identify=true
        },
        fileChanged(){
          let image_file=this.$refs.file.files[0]
          console.log(image_file)
          const item = {
            name: image_file.name,
            size: image_file.size,
            file: image_file
          };
          this.html5Reader(image_file, item);
          this.image=item
        },
        html5Reader(file, item){
          const reader = new FileReader();
          reader.onload = (e) => {
            this.$set(item, 'src', e.target.result)
          };
          reader.readAsDataURL(file)
        },
        submit(){
          if(!this.image){
            this.hint_image='请选择图片'
            return
          }
          if(!this.name){
            this.hint_name='请输入组织名称'
            this.$refs.identify_name.style.border='0.0625rem solid #ff0000'
            return
          }
          if(!this.teacher){
            this.hint_teacher='请输入指导老师'
            this.$refs.identify_teacher.style.border='0.0625rem solid #ff0000'
            return
          }
          let data=new FormData
          data.append('image',this.image)
          data.append('name',this.name)
          data.append('teacher',this.teacher)
          certification(data).then((res)=>{
            this.hint_result='后台认证中'
          }).catch((res)=>{
            console.log(res)
          })
        },
        cleanBorder(){
          if(this.name){
            this.hint_name=''
            this.$refs.identify_name.style.border='0.0625rem solid #cecece'
          }
          if(this.teacher){
            this.hint_teacher=''
            this.$refs.identify_teacher.style.border='0.0625rem solid #cecece'
          }
        }
      },


    }
</script>

<style scoped>
  input[type='file']{
    display: none;
  }
  .input{
    width: 100%;
    line-height: 1.5rem;
    border: 0.0625rem solid #cecece;
    text-indent: 1rem;
    height: 3rem;
  }
  .editBox{
    width: 100vw;
    height: 100vh;
    background-color: rgba(0,0,0,0.8);
    position: fixed;
    top: 0;
    left: 0;
    z-index: 100;
    box-sizing: content-box;

  }
  #editProfile{
    margin: 10rem auto;
    background-color: #f7fafb;
    width: 58.5rem;
    height: 38.31rem;
    padding: 45px 48px 44px;
    box-shadow: black;
    z-index: 1;
    transition: all 1s;
    -moz-transition: all 1s;
    -webkit-transition: all 1s;
    -o-transition:all 1s;
  }
  .scale1{
    transform: scale(1);
  }
  #userimage-area{
    width: 47%;
    height: 100%;
    float: left;
    background-color: #e4f3f6;
    position: relative;
  }

  #userimage-area span.center-text{
    width: 4.5rem;
    height: 4.5rem;
    line-height: 4.5rem;
    border-radius: 4.5rem;
    background-color: #2cbec6;
    position: absolute;
    top:0;right: 0;bottom: 0;left: 0;
    margin: auto;
    overflow: hidden;
    font-size: 5rem;
    cursor: pointer;
  }
  .image-identify{
    width: 100%;
  }
  .center-text{
    text-align:center;
    font-size: 3rem;
    line-height: 4.6875rem;
    color: white;
  }
  span.user-material{
    color:#9fa0a1;
    position: absolute;
    top: 60%;
    left:0;
    right: 0;
    margin: auto;
  }
  #type-area{
    width: 53%;
    height: 100%;
    float: left;
    text-align: left;
    padding: 3rem 2.625rem;
  }
  #type-area p {
    text-align: left;
    font-weight: 700!important;
  }
  .typearea-line{
    width: 100%;
  }
  #typearea-btn{
    padding: 3rem 0;
  }
  .bottom{
    margin-left: 1rem;
    height: 3rem;
    width: 7rem;
    color: #fff;
    background: #9ad4e2;
    border: none;
    border-radius: 3rem;
    float: right;
    font-size: 1.25rem;
    cursor: pointer;
  }
  .confirm:hover{
    background: #2cbec6;
  }
  .cancel{
    background: #e9e9e9;
  }
  .cancel:hover{
    background: #BEBEBE;
  }
  input[type='text']:focus{
    border: 0.0625rem solid #5bc3dc;
  }

</style>



