<template>
    <div class="upload ">
      <tslg_header/>
      <div class="upload-box clear">
      <div class="left">
        <div>
          <div v-for="(file, index) of result" class="file-item-wrap">
            <div class="file-item" >
              <div class="img-box" v-if="!file.pre_file">
                <div class="up-pre-img">
                  <img src="../../assets/big_icon/upload.png" @click="showUploadPre(index)">
                  <span>上传预览图</span>
                </div>
                <span class="file-remove" @click="remove(index)" title="删除">×</span>
              </div>
            <div v-if="file.pre_file" class="pre-img">
              <img :src="file.pre_file.src">
              <div class="up-pre-img" :class="{editing:file.edit_status}" v-if="!file.upload_status">
                <img src="../../assets/big_icon/upload_edit.png" @click="edit(index)" v-if="!file.edit_status">
                <span v-if="!file.edit_status">编辑</span>
                <img src="../../assets/big_icon/upload_edit.png" @click="cancelEdit(index)" v-if="file.edit_status">
                <span v-if="file.edit_status">取消编辑</span>
              </div>
              <div class="up-pre-img" v-show="file.upload_status">
                <canvas ref="canvas_upload" :width="canvas_width" :height="canvas_width" class="upload-progress-canvas"></canvas>
                <span style="margin-top: .5rem">{{progress+'%'}}</span>
              </div>
              <span class="file-remove" @click="remove(index)" title="删除">×</span>
            </div>
            </div>
            <input type="text" class="name-input" v-model="file.name" @blur="changeFileName(file,file.name)"/>

          </div>
          <div v-if="status === 'ready'" class="add">
              <i class="add-icon" @click="add" title="点击选择文件"></i>
          </div>
        </div>
        <input type="file" class="file-input" @change="fileChanged" ref="file" multiple="multiple">
      </div>


      <div class="right">
        <div class="top-btn"><div @click="showUploadSome">批量上传预览图</div></div>
        <div class="content-wrap">
          <div class="cover" v-if="cur_edit_list.length===0"></div>
          <div class="edit-num">编辑已选的{{cur_edit_list.length}}张图片</div>
          <div class="cate">
            <h3>分类</h3>
            <input type="text" v-model="cur_cates" class="cate-input" readonly @click="showChoiceCate">
            <div class="cate-choice" v-if="show_choice_cate">
              <div class="top">
                <span v-for="(item,index) in cate_level" :class="{on_cate:index===cIndex}" @click="choiceLevel(index)">{{item}}</span>
              </div>
              <div class="cate-item">
                <span v-for="(item,index) in cates" v-if="cIndex===0" @click="choiceCate1(item)">{{item.name}}</span>
                <span v-for="item in second_cate" v-if="cIndex===1" @click="choiceCate2(item)">{{item.name}}</span>
                <span v-for="item in third_cate" v-if="cIndex===2" @click="choiceCate3(item)">{{item.name}}</span>
              </div>
            </div>
          </div>
          <h3 style="margin: 2rem 0 1rem 0;">关键字<span style="font-size: 1rem; color: #ffd100;"> 3-8个</span></h3>
          <div class="key-word clear">
            <span v-for="(item,index) in cur_key_word_list" class="key-word-item"><span>{{item}}</span><a @click="deleteKeyWord(index)">×</a></span>
            <input placeholder="输入关键字 回车即可添加" type="text" v-model="key_word" @keyup.enter="setKeyWord" @input="keyWordInput"/>
          </div>
          <div class="desc">
            <h3>描述</h3>
            <textarea placeholder="请告诉我们作品背后的故事" v-model="cur_desc" @blur="setDesc"></textarea>
          </div>
          <div class="sbm-btn">
            <input type="button" value="提交全部作品" @click="submit(2)" class="sbm-input"/>
          </div>
        </div>
      </div>
      </div>
      <upload_single ref="upload_single" @getFile="getPreImg"/>
      <upload_some ref="upload_some" :success_img="success_img" @matchFile="matchFile"/>
      <hint ref="hint"/>
      <confirm ref="confirm" @confirm="confirm"/>
      <tslg_footer/>
    </div>
</template>

<script>
  import tslg_header from '../../components/body/tslg_header'
  import tslg_footer from '../../components/body/tslg_footer'
  import upload_single from './upload_single'
  import hint from '../../components/hint'
  import confirm from '../../components/confirm_box'
  import axios from '../../utils/axios'
  import upload_some from './upload_some'
    export default {
        name: "index",
      components:{
        tslg_header,
        tslg_footer,
        upload_single,
        hint,
        confirm,
        upload_some,
      },
      data(){
          return {
            status: 'ready',
            pre_index:0,  //单张上传索引
            result:[],
            edit_index:-1,  //编辑索引
            cate_level:['一级分类','二级分类','三级分类'],
            array_cate:[],
            second_cate:[],
            third_cate:[],
            cIndex:0,
            show_choice_cate:false,
            key_word:'',  //用户单次输入的关键词
            progress:0,   //上传进度
            to:'',    //前往的目标页面
            show_upload_some:false,
            success_img:0,
            cur_cates:'',
            cur_key_word_list:[],
            cur_desc:'',
            cur_edit_list:[],
          }
      },
      computed:{
        cates(){
          return this.$store.state.imageGroup.title
        },
        canvas_width(){
          return document.documentElement.clientWidth*3.125/120
        },
      },
      created(){
          let item=this.$store.state.image.edit_item;
          if(item.id){
            this.result.push(item);
            this.cur_edit_list=this.result
          }
          document.documentElement.scrollTop=0
      },
      beforeRouteLeave(to,from,next){
          if(this.result.length){
            this.$refs.confirm.showConfirm('是否要将未上传的文件保存到草稿箱')
          }else{
            next()
          }
         this.to=to.name
      },
      methods:{
        add(){
          this.$refs.file.click();
          this.cur_cates='';
          this.cur_key_word_list=[];
          this.cur_desc=''
        },
        async fileChanged() {
          const list = this.$refs.file.files;
          let hint_title='';
          for (let input_item of list) {
            if (!this.isContain(input_item)) {
              if(this.result.length<15){
                let obj=new Object();
                obj.cates='';
                obj.key_word_list=[];
                obj.desc='';
                obj.file=input_item;
                obj.name=this.setFileName(obj.file.name);
                obj.upload_status=false;
                obj.edit_status=true;
                await this.addSrc(input_item,obj);
                this.result.push(obj);
              }
              this.cur_edit_list=this.result;
              if(this.result.length>=15){
                this.status='full'
              }
            }else{
              hint_title=hint_title+input_item.name+" ";
            }
          }
          if(hint_title){
            this.$refs.hint.showHint(`${hint_title}已被选择`)
          }
          this.$refs.file.value=''
        },
        async addSrc(pre,org){
          return new Promise((resolve)=>{
            let img=new Image();
            const reader = new FileReader();
            reader.readAsDataURL(pre)
            reader.onload = (e) => {
              pre.src=e.target.result
              img.src=e.target.result
            };
            img.onload=()=>{
              let client_width=document.documentElement.clientWidth*24.75*16/1920,client_height=document.documentElement.clientWidth*18.54*16/1920;
              if(img.width>=client_width/2&&img.height>=client_height)
                this.$set(org,'pre_file',pre)
              resolve()
            };
          })

        },
        html5Reader(file, item){
          const reader = new FileReader();
          reader.readAsDataURL(file)
          reader.onload = (e) => {
            this.$set(item, 'src', e.target.result)
          };
        },
        isContain(file) {
          for (const item of this.result){
            if(item.file.name===file.name||item.size===file.size)
              return true
          }
          return false
        },
        remove(index) {
          this.result.splice(index, 1);
          if(this.result.length===14)
          this.status='ready'
        },
        showUploadPre(index){
          this.pre_index=index
          this.$refs.upload_single.showUploadPre()
          document.documentElement.style.overflow='hidden'
        },
        getPreImg(file){
          let s_file={
            name:file.name,
            size:file.size,
            file:file
          }
          this.html5Reader(file,s_file)
          this.$set( this.result[this.pre_index],'pre_file',s_file)
        },
        //确定编辑的文件
        edit(index){
          for(let item of this.result){
            item.edit_status=false
          }
          this.result[index].edit_status=true;
          this.cur_edit_list.splice(0,this.cur_edit_list.length,this.result[index])
          this.cur_cates= this.result[index].cates;
          this.cur_desc=this.result[index].desc;
          this.cur_key_word_list=this.result[index].key_word_list
          // this.cur_edit_list.splice(0,this.cur_edit_list.length,this.result[index])
        },
        //取消编辑
        cancelEdit(index){
          this.result[index].edit_status=false;
          this.cur_edit_list=[];
          for(let item of this.result){
            if(item.edit_status)
              this.cur_edit_list.push(item)
          }
        },
        editContent(edit,content){
          for(let item of this.cur_edit_list){
              item[`${edit}`]=content
          }
        },
        choiceLevel(index){
          this.cIndex=index
        },
        choiceCate1(item){
          this.editContent("cates",item.name+" > ")
          if(item.kids.length){
            this.second_cate=item.kids;
            this.cur_cates=item.name+' > ';
            this.cIndex=1
          }else{
            this.cur_cates=item.name;
            this.showChoiceCate()
          }
        },
        choiceCate2(item){
          this.cur_cates = this.cur_cates.split(" > ")[0] + ' > ' + item.name;
          if(item.kids.length){
            this.third_cate=item.kids;
            this.cur_cates = this.cur_cates + " > ";
            this.cIndex= 2
          }else this.showChoiceCate()
          this.editContent("cates",this.cur_cates)
        },
        choiceCate3(item){
          let new_array = this.cur_cates.split(" > ");
          if(new_array.length>2)
            new_array.pop();
          new_array=new_array.join(" > ");
          this.cur_cates = new_array + " > " + item.name;
          this.showChoiceCate()
          this.editContent("cates",this.cur_cates)
        },
        showChoiceCate(){
          this.show_choice_cate=!this.show_choice_cate;
          this.cIndex=this.cur_edit_list[0].cates.split(" > ").length-1;
          this.array_cate=[]
        },
        setKeyWord(){
          this.key_word=this.key_word.trim()
          if(this.key_word){
            if(this.cur_edit_list[0].key_word_list.length<8){
              for(let item of this.cur_edit_list){
                item.key_word_list.push(this.key_word)
              }
              this.cur_key_word_list.push(this.key_word)
            }
            else {
              this.$refs.hint.showHint('关键词数量不超过8个')
            }
          }
          this.key_word=''
        },
        setDesc(){
          this.editContent("desc",this.cur_desc)
        },
        deleteKeyWord(index){
          this.key_word_list.splice(index,1)
        },
        uploadProgress(progress){
          progress=progress/50;
          let c=this.$refs.canvas_upload[0];
          let width=this.canvas_width;
          let ctx=c.getContext('2d');
          ctx.clearRect(0,0,width,width)
          ctx.beginPath();
          ctx.arc(width/2,width/2,width/2,0,progress*Math.PI);
          ctx.lineTo(width/2,width/2);
          ctx.fillStyle='#ffffff';
          ctx.fill();
          ctx.closePath()
        },
        async submit(index){
          let result=[...this.result];
          for(let r_item of result){
            let formData=new FormData;
            formData.append('if_active',index);
            if(r_item.file){
              if(r_item.file.type.indexOf('image')!==-1)
                formData.append('ori_img',r_item.file);
              else formData.append('file',r_item.file);
              formData.append('name',r_item.name);
              formData.append('image',r_item.pre_file);
            }
            if(r_item.pre_file&&r_item.cates&&r_item.desc){
              if(r_item.key_word_list.length<3){
                this.$refs.hint.showHint('关键词不得少于三个');
                return
              }
              r_item.upload_status=true;
              formData.append('desc',r_item.desc);
              formData.append('cates',r_item.cates.split(" > ").pop());
              formData.append('keywords',r_item.key_word_list.join(" "));
            }else if(index===4){
              r_item.upload_status=true;
              if(r_item.pre_file)
                formData.append('image',r_item.pre_file);
              if(r_item.desc)
                formData.append('desc',r_item.desc);
              if(r_item.cates.split(" > ").pop())
                formData.append('cates',r_item.cates.split(" > ").pop());
              if(r_item.key_word_list.join(" "))
                formData.append('keywords',r_item.key_word_list.join(" "))
            }else{
              this.$refs.hint.showHint('请完善上传信息');
              return
            }
            if(r_item.id)
              await this.setUpload(formData,r_item.id);
            else
              await this.setUpload(formData);
          }
            this.$refs.hint.showHint('上传成功')
        },
        async setUpload(formData,sw) {
          let config = {
            headers: {
              'Content-Type': 'multipart/form-data'
            },
            onUploadProgress: (progressEvent) => {
              // 使用本地 progress 事件
              if (progressEvent.lengthComputable) {
                let num = Math.round((progressEvent.loaded / progressEvent.total) * 100);
                this.progress=num;
                this.uploadProgress(num)
              }
            }
          };
          return await new Promise((resolve, reject) => {
            if(sw){
              axios.put(`/images/${sw}/`,formData,config).then(()=>{
                if(this.progress===100){
                  this.remove(0);
                  this.progress=0;
                  resolve()
                }
              }).catch(()=>{
                this.$refs.hint.showHint('上传失败 请重新上传');
                reject()
              })
            }else{
              axios.post('/images/',formData,config).then(()=>{
                if(this.progress===100){
                  this.remove(0);
                  this.progress=0;
                  resolve()
                }
              }).catch(()=>{
                this.$refs.hint.showHint('上传失败 请重新上传');
                reject()
              })
            }
          })
        },
        keyWordInput(){
          if(this.key_word.length>4){
            this.key_word=this.key_word.substring(0,4)
            this.$refs.hint.showHint('关键词不超过4个字')
          }
        },
        async confirm(status){
          if(status){
            await this.submit(4);
            this.$router.push({name:`${this.to}`})
          }else{
            this.result=[];
            this.$router.push({name:`${this.to}`})
          }
        },
        changeFileName(file,name) {
          if(name.length>10){
            this.$refs.hint.showHint('文件名称长度不得超过10')
            name=name.substring(0,10)
          }
          file.name=name
        },
        showUploadSome(){
          this.$refs.upload_some.showUploadSome()
        },
        setFileName(str){
          let a_str=str.split(".");
          a_str.pop();
          return a_str.join(".")
        },
        matchFile(m_file){
          let suc=0;
          for (const org of this.result){
            for(const pre of m_file){
              if(!org.pre_file){
                if(org.name===this.setFileName(pre.name)){
                  this.addSrc(pre,org)
                  suc++
                }
              }
            }
          }
          this.success_img=suc;
          this.$refs.hint.showHint(`成功匹配${suc}组图片`)
        }
      }
    }
</script>

<style lang="scss" scoped>
  @import "../../styles/variables";
  .upload{
    background: $bg;
    margin: 0 auto;
  }
  .upload-box{

  }
  .left{
    width: 93.3475rem;
    height: 63.5rem;
    float: left;
    padding: 1.6875rem .9375rem 1.375rem;
  }
  .right{
    float: left;
    background: #fff;
    width: 25.34rem;
    height: 63.5rem;
  }
  .file-item-wrap{
    width: 16.44rem;
    margin: 0 .927rem 1.25rem;
    float: left;
    .name-input{
      width: 100%;
      height: 1.9375rem;
      background: $bg;
      font-size: 1.125rem;
      &:hover{
        text-indent: .5rem;
        background: #fff;
        border: 0.0625rem solid $normal;
      }
    }
  }
  .file-item {
    position: relative;
    display: flex;
    align-items: center;
    justify-content: center;
    float: left;
    width: 16.44rem;
    height: 16.44rem;
    text-align: center;
    margin-bottom: .75rem;
    border: 0.0625rem solid #dadada;
    background-color: #ececec;
    .img-box{
      position: relative;
      height: 16.44rem;
      width: 16.44rem;
    }
  }
  .up-pre-img{
    position: absolute;
    top: 0;
    left: 0;
    display: flex;
    justify-content: center;
    align-items: center;
    flex-direction: column;
    height: 100%;
    min-height: 5rem;
    width: 100%;
    color: #fff;
    background: rgba(0,0,0,.4);
    img{
      display: inline-block;
      height: 3.125rem;
      width: 3.125rem;
      margin-bottom: .5rem;
    }
  }
  .file-remove {
    position: absolute;
    right: 0;
    top: 0;
    width: 2rem;
    height: 2rem;
    color: white;
    cursor: pointer;
    line-height: 2.5rem;
    font-size: 2.5rem;
    border-radius: 100%;
  }
  .add {
    float: left;
    display: flex;
    align-items: center;
    justify-content: center;
    width: 16.44rem;
    height: 16.44rem;
    margin: 0 .927rem 1.25rem;
    border: 0.0625rem solid #dadada;
    background-color: #ececec;
    .add-icon{
      cursor: pointer;
      background: url(../../assets/big_icon/add.png);
      width: 3.75rem;
      height:3.75rem;
      display: inline-block;
      -webkit-background-size: cover;
      background-size: cover;
    }
  }
  .file-input{
    display: none;
  }

  .pre-img{
    position: relative;
    max-width: 16.44rem;
    max-height: 16.44rem;
    img{
      max-width: 16.44rem;
      max-height: 16.44rem;
    }
  }
  .editing{
    border: 0.2rem solid $normal;
  }

  /*
  right
   */
  .top-btn{
    height: 5rem;
    padding: 1rem 1.875rem;
    border-bottom: 0.0625rem solid #e9e9e9;
    div{
      height: 3rem;
      background: $normal;
      color: $f-deep;
      font-weight: bold;
      line-height: 3rem;
      border-radius: 3rem;
      cursor: pointer;
      &:hover{
        background: $hover;
      }
    }
  }
  .content-wrap{
    position: relative;
    padding: 0 1.875rem;
    text-align: left;
  }
  .edit-num{
    margin: 1rem 0 3rem 0;
    font-size: 1.25rem;
    color: #f5a623;
  }
  .cate{
    position: relative;
    h3{
      font-size: 1.125rem;
      margin: 0 0 1rem 0;
    }
  }
  .cate-input{
    border: 0.0625rem solid $normal;
    font-size: 1rem;
    text-indent: .75rem;
    width: 100%;
    height: 3rem;
  }
  .cate-choice{
    position: absolute;
    z-index: 1;
    width: 100%;
    border: 0.0625rem solid $normal;
  }
  .cate-choice > .top{
    height: 3rem;
    background: #f5f5f4;
    span{
      text-align: center;
      display: inline-block;
      width: 33.3%;
      line-height: 3rem;
      font-size: 1rem;
      cursor: pointer;
    }
  }
  .cate-item{
    padding: 0.375rem 0 0.625rem 0;
    min-height: 4.5rem;
    background: #fff;
    span{
      text-align: center;
      display: inline-block;
      width: 33.3%;
      height: 1.75rem;
      line-height: 1.75rem;
      font-size: 1rem;
      cursor: pointer;
      &:hover{
        color: $normal;
      }
    }
  }
  .on_cate{
    background: #fff;
  }
  .key-word{
    padding: .5rem;
    border: 0.0625rem solid #e9e9e9;
    height: 9rem;
    overflow: hidden;
    input{
      width: 100%;
      height: 2rem;
      font-size: 1rem;
    }
  }
  .key-word-item{
    position: relative;
    height: 1.5625rem;
    background: $normal;
    font-size: 1rem;
    float: left;
    margin: 0 .5rem .5rem 0;
    color: #fff;
    padding-right: 1.4rem;
    padding-left: .5rem;
    line-height: 1.5625rem;
    a{
      position: absolute;
      right: 0;
      height: 100%;
      width: 1.3rem;
      color: #fff;
      text-align: center;
      font-size: 1.5rem;
      &:hover{
        background: $hover;
      }
    }
  }
  .desc{
    textarea{
      width: 100%;
      height: 9rem;
      resize: none;
      font-size: 1rem;
      padding: .5rem;
      overflow: hidden;
    }
  }
  .sbm-btn{
    margin-top: 3rem;
  }
  .sbm-input{
    width: 100%;
    height: 3rem;
    -webkit-border-radius: 3rem;
    -moz-border-radius: 3rem;
    border-radius: 3rem;
    line-height: 3rem;
    background: $normal;
    color: $f-deep;
    font-size: 1.2rem;
    font-weight: 600;
    cursor: pointer;
  }

  .upload-progress-canvas{
    border: .25rem #fff;
    border-radius: 50%;
  }

  .cover{
    position: absolute;
    z-index: 2;
    top: 0;
    left: 0;
    background: rgba(255,255,255,.7);
    height: 100%;
    width: 100%;
  }
</style>
