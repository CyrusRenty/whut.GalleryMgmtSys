<template>
  <div class="wrap">
  <div class="person-works clear">
    <div class="left-nav">
      <router-link class="nav-item" to="upload">我的上传</router-link>
      <router-link class="nav-item" to="download">我的下载</router-link>
    </div>
    <router-view/>
  </div>
  </div>
</template>

<script>
    export default {
        name: "index"
    }
</script>

<style lang="scss" scoped>
  @import "../../../styles/variables";
  .wrap{
    width: 100%;
    background: #f4f4f4;
  }
  .person-works{
    width: 107rem;
    margin: 0 auto;
    padding: 3rem 0 5rem 0;
  }
  .left-nav{
    display: inline-block;
    width: 19rem;
    height: 8rem;
    background: #fff;
    float: left;
    margin-right: 3rem;
  }
  .nav-item{
    display: block;
    height: 50%;
    color: $f-deep;
    line-height: 4rem;
    font-size: 1.25rem;
    text-align: right;
    padding-right: 10.875rem;
    &:hover{
      color: $normal;
    }
  }
  .router-link-active{
    color: $normal;
    border-left: 0.125rem solid $normal;
  }
</style>
