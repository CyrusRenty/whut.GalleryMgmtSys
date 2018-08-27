<template>
    <div class="upload-card" >
      <div class="upload-wrap">
        <i @click="showUpLoad"></i>
        <span class="suggest-text">上传</span>
      </div>
    </div>
</template>

<script>
    export default {
        name: "upload_card",
        methods:{
          showUpLoad(){
            document.body.style.overflow = 'hidden';
            this.$router.push('upload/uploader')
          },
        }
    }
</script>

<style scoped>
.upload-card{
  float: left;
  width: 24.4rem;
  height: 32.3rem;
  margin: 0 1.5rem 3rem 1.5rem;
  background: #e4f2f5;
}
i{
  background: url(../../assets/Add.png);
  background-size: 100% 100%;
  height: 7rem;
  width: 7rem;
  cursor: pointer;
}
.suggest-text{
  font-size: 1.5rem;
  margin-top: 2rem;
}

.upload-wrap{
  display: flex;
  justify-content: center;
  align-items: center;
  width: 100%;
  height: 100%;
  flex-direction: column;
}


</style>
