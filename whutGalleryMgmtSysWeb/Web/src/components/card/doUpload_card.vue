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
            this.$router.push('/tslg/doUpload')
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
  background: #fff;
}
i{
  background: url(../../assets/big_icon/add.png);
  background-size: 100% 100%;
  height: 4.7rem;
  width: 4.7rem;
  cursor: pointer;
}
.suggest-text{
  font-size: 1.5rem;
  margin-top: 1rem;
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
