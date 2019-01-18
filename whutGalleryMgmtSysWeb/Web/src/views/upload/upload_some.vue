<template>
    <div class="upload-some" v-if="show_upload_some">
      <div class="upload-box">
        <div class="top">
          <span class="title">批量上传预览图</span><span class="notice">预览图与源文件命名必须相同才能匹配成功</span>
          <span @click="closePage" class="close">×</span>
        </div>
        <div class="middle">
          <i @click="choiceFile"></i>
          <span>上传图片</span>
          <span>支持JPG、PNG，大小不超过5M</span>
          <span>建议尺寸800*600</span>
          <span>最小尺寸400*300</span>
        </div>
        <div class="bottom">已添加{{add_img}}张图片，匹配成功{{success_img}}张图片</div>
      </div>
      <input type="file" accept="image/*" multiple="multiple" ref="input" style="display: none;" @change="fileChanged"/>
    </div>
</template>

<script>
    export default {
        name: "upload_some",
      props:['success_img'],
      data(){
          return {
            show_upload_some:false,
            add_img:0,
          }
      },
      methods:{
        showUploadSome(){
          this.show_upload_some=true;
          document.documentElement.style.overflow='hidden'
        },
        closePage(){
          this.add_img=0;
          this.show_upload_some=false;
          document.documentElement.style.overflow='auto'
        },
        choiceFile(){
          this.$refs.input.click()
        },
        fileChanged(){
          let file_list=[],file_list1=this.$refs.input.files
          for(let item of file_list1){
            let img=new Image(),reader = new FileReader();
            reader.readAsDataURL(item);
            reader.onload=(e)=>{img.src=e.target.result}
            img.onload=()=>{
              if(img.width>400&&img.height>300){
                file_list.push(item)
              }
            }
          }
          this.add_img=this.add_img+file_list1.length;
          this.$emit('matchFile',file_list);
        },
      }
    }
</script>

<style scoped>
  .upload-some{
    position: fixed;
    top: 0;
    height: 100%;
    width: 100%;
    z-index:3;
    display: flex;
    justify-content: center;
    align-items: center;
    background: rgba(0,0,0,.4);
  }
  .upload-box{
    width: 58.5rem;
    height: 34rem;
    padding: 1.5rem 3rem;
    background: #fff;
  }
  .top{
    position: relative;
    text-align: left;
  }
  .title{
    font-size: 1.25rem;
    font-weight: 600;
  }
  .notice{
    font-size: .875rem;
    color: #f79e00;
    margin-left: .75rem;
  }
  .close{
    position: absolute;
    right: 0;
    top: -1rem;
    font-size: 3rem;
    cursor: pointer;
  }
  .middle{
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    width: 52.5rem;
    background: #f5f5f4;
    height: 25rem;
    margin: 1.5rem 0;
  }
  .middle i{
    display: inline-block;
    width: 4.6875rem;
    height: 4.6875rem;
    background: url(../../assets/big_icon/add.png) no-repeat center;
    -webkit-background-size: cover;
    background-size: cover;
    cursor: pointer;
  }
  .middle span{
    color: #9b9b9b;
  }
  .middle span:nth-child(2){
    color: #000;
    margin: .75rem 0;
    font-size: 1.125rem;
  }
  .bottom{
    color: #f79e00;
    font-size: 1.125rem;
  }

</style>
