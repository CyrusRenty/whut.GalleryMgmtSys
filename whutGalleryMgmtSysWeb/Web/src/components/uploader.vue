<template>
  <div class="uploaderBox" @click="hide_uploader">
    <div class="vue-uploader"  ref="uploader" @click.stop="not_hide_uploader">
      <img id="thumbnail" class="thumbnail" @click="hide()" title="点击收回原图" />

        <div class="file-list">
            <section v-for="(file, index) of files" class="file-item draggable-item">
                <img :src="file.src" alt="" ondragstart=" false;" @click="showView(file.src)" title="点击查看原图">
                <span class="file-remove" @click="remove(index)" title="删除图片">+</span>
            </section>
            <section id="add_btn" v-if="status === 'ready'" class="file-item" ref="add_btn">
                <div class="add">
                  <i class="add-icon" @click="add" title="点击选择图片"></i>
                </div>
              <div class="hint set_text_align_left">{{hint_image}}</div>
            </section>
        </div>
      <input type="file" accept="image/*" @change="fileChanged" ref="file" multiple="multiple">

      <div class="upload-info">
        <form class="form-wrap">
          <span class="h22 fl s-mar" >作品分类</span><span>（最多可选四项）</span>
          <div v-for="(list,index) in cates_box"  class="onecate" >
            <span class="upload-cates">{{list.cate_name}}</span>
            <label v-for="(item, key) in list.cate_choice" class="upload-choice" >
            <input type="checkbox" :id="'check'+3*(index+key*4)" name="checkbox" @click="set_checkbox(index,key,item)" ref="checkbox"/>
              <label :for="'check'+3*(index+key*4)" >{{item.choice_name}}</label>
            </label>
            <br/>
          </div>
          <div class="hint">{{hint_checkbox}}</div>
          <br/><span class="h22 fl">作品命名</span><br/><input class="input-name" type="text" v-model="name" @input="uploadName" ref="upload_name" @blur="cleanBorder"><br/>
          <div class="hint">{{hint_works_name}}</div>
          <br/><span class="h22 fl  ">作品简介</span><br/><textarea class="input-desc" v-model="desc" rows="5" cols="49" placeholder="（不超过八十字）" @input="uploadDesc" ref="upload_desc" @blur="cleanBorder"></textarea>
          <div class="hint">{{hint_works_desc}}</div>
        </form>
        <section  class="upload-func" >
          <div v-if="uploading">
            <div class="hint">成功上传{{hint_upload_num}}个作品</div>
            <div class="progress-bar" >
              <div :style="{'width':percent+'%'}">{{percent+ '%'}}</div>
            </div>
          </div>
        </section>
        <div class="bottom-btn">
          <div class="hint">{{progress}}</div>
          <div class="sc-btn">
            <input type="button" class="cancel" value="返回" @click="hide_uploader"/>
            <input type="button" class="submit" value="上传" @click="submit" />
          </div>

        </div>
      </div>
    </div>
  </div>
</template>
<script>
  import {upload} from "../api/user";
  import axios from '../utils/axios'
  import cookie from "../utils/cookie";
  export default {
        data() {
            return {
                status: 'ready',
                name:'',
                files: [],
                point: {},
                uploading: false,
                progress:'',
                percent:0,
                cates:'',
                array_cate:[],
                cates_box:[
                  {cate_name:'菁菁校园', cate_choice:[{choice_name:'校园风景'}, {choice_name:'校园活动'}, {choice_name:'学子风采'},]},
                  {cate_name:'摄影艺术', cate_choice:[{choice_name:'生活'}, {choice_name:'风景'}, {choice_name:'人物'},]},
                  {cate_name:'办公创意', cate_choice:[{choice_name:'PPT'}, {choice_name:'简历'}, {choice_name:'WORD'},]},
                  {cate_name:'平面设计', cate_choice:[{choice_name:'PS'}, {choice_name:'手绘'}, {choice_name:'合成图'},]},
                ],
                desc:'',
                upload_height:0,
                hint_image:'',
                hint_checkbox:'',
                hint_works_name:'',
                hint_works_desc:'',
                hint_upload_num:0,
            }
        },
        methods: {
            add() {
                this.$refs.file.click()
              this.hint_image=''
            },
            set_checkbox(index,key,e){
              let nIndex=index*3+key
              this.hint_checkbox=''
                if(this.$refs.checkbox[nIndex].checked){
                  this.array_cate.push(e.choice_name)
                }else{
                  let nIndex=this.array_cate.indexOf(e.choice_name)
                  this.array_cate.splice(nIndex,1)
                }
                if(this.array_cate.length===4){
                  for(let i=0;i<12;i++){
                      if(!this.$refs.checkbox[i].checked){
                        this.$refs.checkbox[i].disabled='disabled'
                    }
                  }
                }
                if(this.array_cate.length<4&&this.array_cate.length>0){
                  for(let i=0;i<12;i++){
                    this.$refs.checkbox[i].disabled=false
                  }
                }
                console.log(this.array_cate)
            },
            async submit() {
              this.cates=this.array_cate.join(" ")
              console.log(this.cates)
              if (this.files.length === 0) {
                  this.hint_image='请选择图片'
                  return
              }
              if(this.cates===''){
              this.hint_checkbox='请选择作品分类';
              return
            }
              if(!this.name){
              this.hint_works_name='请填写作品名称'
              return
            }
              if(this.desc===''){
                  this.hint_works_desc='请填写作品简介';
                  return
              }
              let length=this.files.length
              for(let i=0;i<length;i++) {
                this.uploading = true;
                let formData = new FormData();
                this.progress='上传中'
                formData.append('image', this.files[0].file);
                formData.append('desc', this.desc);
                formData.append('cates', this.cates);
                formData.append('name', this.name);
                await this.setUpload(formData)
              }
              this.finished()
            },
          async setUpload(formData) {
            let config = {
              headers: {
                'Content-Type': 'multipart/form-data'
              },
              onUploadProgress: (progressEvent) => {
                // 使用本地 progress 事件
                if (progressEvent.lengthComputable) {
                  let num = Math.round((progressEvent.loaded / progressEvent.total) * 100)
                  this.percent = num // 使用某种 UI 进度条组件会用到的百分比
                }
              }
            }
            return await new Promise((resolve, reject) => {
              axios.post('/images/',formData,config).then((res)=>{
                if(res.data){
                  if(this.percent===100){
                    this.remove(0)
                    this.uploading=false
                    this.hint_upload_num++
                    resolve()
                  }
                }else{
                  this.progress='上传失败 请返回重新上传'
                  reject()
                }
              }).catch(()=>{
                this.progress='上传失败 请返回重新上传'
                reject()
              })
            })
          },
            finished() {
              this.progress='上传成功 后台审核中'
              setTimeout(()=>{this.progress=''},1800)
                for(let i=0;i<12;i++)
                    this.$refs.checkbox[i].checked=false
                this.hint_upload_num=0
                this.name='';
                this.cates='';
                this.desc='';
                this.status = 'ready'
            },
            remove(index) {
                this.files.splice(index, 1);
                this.hide();
                this.$refs.add_btn.style.display='block'
            },
            fileChanged() {
              const list = this.$refs.file.files;
              for (let i = 0; i < list.length; i++) {
                if (!this.isContain(list[i])) {
                  const item = {
                    name: list[i].name,
                    size: list[i].size,
                    file: list[i]
                  };
                  this.html5Reader(list[i], item);
                  if(this.files.length<12){
                    this.files.push(item)
                  }
                  if(this.files.length>=12){
                    this.$refs.add_btn.style.display='none'
                  }
                  //console.log(this.files)
              }else{
                  this.hint_image='该图片已被选择'
                }
              }
              this.$refs.file.value = ''
            },
            // 将图片文件转成BASE64格式
            html5Reader(file, item){
                const reader = new FileReader();
                reader.onload = (e) => {
                    this.$set(item, 'src', e.target.result)
                };
                reader.readAsDataURL(file)
            },
            isContain(file) {
              let a=this.files.find((item)=>{
                if (item.name===file.name&&item.size===file.size)
                  return true
              })
               if(a){
                 return true
               }
              else return false
            },

            showView(src){
                var upload = this.$refs.uploader;
                let view  = document.getElementById('thumbnail');
                view.src = src;
                view.style.display = 'inline';
                this.center_uploader()
            },
            hide(){
                let view  = document.getElementById('thumbnail');
                view.src='';
                view.style.display = 'none';
                this.center_uploader()
            },
            center_uploader(){
                const heightCss = window.getComputedStyle(this.$refs.uploader).height;
                this.$refs.uploader.style.marginTop = 'calc(50vh - ' + parseInt(heightCss)/2 + 'px)';
            },
            hide_uploader(){
                this.$router.go(-1);
                document.body.style.overflow = 'auto';
            },
            not_hide_uploader(){

            },
            uploadName(){
            if(this.name.length>6){
              let length=0
              for(var i=0;i<this.name.length;i++){
                var a=this.name.charAt(i)
                if (a.match(/[^\x00-\xff]/ig) != null){
                  length+=2
                }else length+=1
              }
              if(length>16){
                this.hint_works_name='作品名称过长'
                this.$refs.upload_name.style.border='#ff0000 0.0625rem solid'
              }else{
                this.hint_works_name=''
                this.$refs.upload_name.style.border='#2cbec6 0.0625rem solid'}
            }else{
              this.hint_works_name=''
              this.$refs.upload_name.style.border='#2cbec6 0.0625rem solid'
            }
          },
            uploadDesc(){
            if(this.desc.length>79){
              let length=0
              for(var i=0;i<this.desc.length;i++){
                var a=this.desc.charAt(i)
                if (a.match(/[^\x00-\xff]/ig) != null){
                  length+=2
                }else length+=1
              }
              if(length>=80){
                this.hint_works_desc='作品简介过长'
                this.$refs.upload_desc.style.border='#ff0000 0.0625rem solid'
              }
              else{
                this.hint_works_desc=''
                this.$refs.upload_desc.style.border='#2cbec6 0.0625rem solid'
              }}
              else{
              this.hint_works_desc=''
              this.$refs.upload_desc.style.border='#2cbec6 0.0625rem solid'
            }
          },
            cleanBorder(){
              if(!this.hint_works_name)
            this.$refs.upload_name.style.border='#cecece 0.0625rem solid'
            if(!this.hint_works_desc)
              this.$refs.upload_desc.style.border='#cecece 0.0625rem solid'
          }
         },
        mounted(){
          document.body.style.overflow = 'hidden';
          const heightCss = window.getComputedStyle(this.$refs.uploader).height;
          this.$refs.uploader.style.marginTop = 'calc(50vh - ' + parseInt(heightCss)/2 + 'px)';
          this.upload_height = parseInt(heightCss)
        }
    }
</script>
<style>
  .uploaderBox{
    width: 100%;
    height: 100%;
    background-color: rgba(0,0,0,0.6);
    position: fixed;
    top: 0;
    left: 0;
    z-index: 100;
  }
.vue-uploader {
    background-color: #f7fafb;
    position: fixed;
    z-index: 100;
    width: 58.5rem;
    top: 0;left: 0;right: 0;
    margin: auto;
    max-height: 100vh;
    overflow-y: scroll;
    overflow-x: hidden;
    transition: all 0.4s ease;
}
.vue-uploader::-webkit-scrollbar { width: 0 !important }
/*.vue-uploader { -ms-overflow-style: none; }*/
/*.vue-uploader { overflow: -moz-scrollbars-none; }*/
 .file-list {
    width: 50%;
    padding: 1.875rem;
    float: left;
}
.file-list:after {
    content: '';
    display: block;
    clear: both;
    visibility: hidden;
    line-height: 0;
    height: 0;
    font-size: 0;
}
 .file-item {
    float: left;
    position: relative;
    width: 6.25rem;
    text-align: center;
    margin-left: 1.875rem;
    margin-bottom: 1.5rem;
    height: 6.25rem;
}
 .file-item img{
    width: 6.25rem;
    max-height: 100%;
    border: 0.0625rem solid #ececec;
}
.vue-uploader .file-list .file-item .file-remove {
    position: absolute;
    right: 0;
    display: none;
    top: 0;
    width: 1.5rem;
    height: 1.5rem;
    color: white;
    cursor: pointer;
    line-height: 1.5rem;
  font-size: 1.5rem;
    border-radius: 100%;
    transform: rotate(45deg);
    background: rgba(0, 0, 0, 0.5);
}
.vue-uploader .file-list .file-item:hover .file-remove {
    display: inline;
}
.thumbnail{
  width: 100%;
  overflow: hidden;
  display: none;
}
 .add {
    width: 6.25rem;
    height: 6.25rem;
    float: left;
    text-align: center;
    line-height: 5rem;
    border: 1px dashed #ececec;
    font-size: 1.875rem;
    background-color: #e4f2f5;
    display: flex;
    align-items: center;
    justify-content: center;
}
 .add-icon{
   cursor: pointer;
   background: url(../assets/Add.png);
   width: 2.5rem;
   height:2.5rem;
   display: inline-block;
   -webkit-background-size: cover;
   background-size: cover;
 }
.vue-uploader .upload-func {
    display: flex;
    margin: 0;
    width: 100%;
    flex-direction: column;
    height: 4rem;
}
.vue-uploader .upload-func .progress-bar {
    width: 100%;
    border: 0.09rem solid #00b4aa;
    border-radius: 1rem;
    height: 1.2rem;
    box-sizing: content-box;
}
.vue-uploader .upload-func .progress-bar div {
    height: 1.2rem;
    background: #00b4aa;
    border-radius: 1rem;
    text-align: center;
    color: #4a4a4a;
    font-size: 0.9rem;
    transition: all .5s ease;
}
.bottom-btn{
  width: 100%;
  text-align: right;
  margin-bottom: 2rem;
}
.vue-uploader > input[type="file"] {
    display: none;
}

.input-desc{
  width: 100%;
  resize:none;
  border: 0.0625rem solid #cecece;
  outline:none;
  line-height: 1.5rem;
  padding: 0 0.4rem;
  font-size:1.2rem;
}
.input-desc:focus{
  border:0.0625rem #2cbec6 solid;
}
.h22{
  font-size: 1.2rem;
}
.fl{
  text-align: left;
}
.upload-choice{
  width: 6rem;
  font-size: 0.875rem;
  display: inline-block;
  position: relative;
}
span.upload-cates{
  display: inline-block;
  width: 7.75rem;
  font-size: 1.125rem;
  font-weight: bold!important;
  line-height: 1.625rem;
}

.onecate{
  text-align: left;
  line-height: 2rem;
}

.upload-info{
  width: 50%;
  float: right;
  padding: 1rem 2rem 0 1rem;
}
.form-wrap{
  text-align: left;
  padding-top:2rem ;
}
.s-mar{
  display: inline-block;
  margin-bottom: 0.5rem;
}
.input-name{
  height: 3rem;
  border: 0.0625rem solid #cecece;
  font-size: 1.2rem;
  line-height: 3rem;
  text-indent: 0.4rem;
  width: 100%;
}
.set_text_align_left{
  text-align:left;
}



/*input样式*/
  input[type="checkbox"]:checked,
  input[type="checkbox"]:not(:checked)
  {
    position: absolute;
    left: -9999px;
  }
  input[type="checkbox"]:checked + label,
  input[type="checkbox"]:not(:checked) + label
  {
    position: relative;
    padding-left: 1.75rem;
    cursor: pointer;
    line-height: 1.25rem;
    display: inline-block;
    color: #666;
  }
  input[type="checkbox"]:checked + label:before,
  input[type="checkbox"]:not(:checked) + label:before
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
  input[type="checkbox"]:checked + label:after,
  input[type="checkbox"]:not(:checked) + label:after
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
  input[type="checkbox"]:not(:checked) + label:after
  {
    opacity: 0;
    -webkit-transform: scale(0);
    -moz-transform: scale(0);
    -o-transform: scale(0);
    -ms-transform: scale(0);
    transform: scale(0);
  }
  input[type="checkbox"]:checked + label:after
  {
    opacity: 1;
    -webkit-transform: scale(1);
    -moz-transform: scale(1);
    -o-transform: scale(1);
    -ms-transform: scale(1);
    transform: scale(1);
  }
  .uploaderBox input[type='text']:focus{
    border: 0.0625rem solid #2cbec6;
  }


</style>
