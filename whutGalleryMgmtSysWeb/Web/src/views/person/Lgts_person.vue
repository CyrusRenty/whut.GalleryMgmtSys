<template>
<div class="person">
  <Lgts_head/>
  <div class="person-top-nav">
    <router-link class="nav-item" to="/tslg/person/person_center">个人主页</router-link>
    <router-link class="nav-item" to="/tslg/person/person_works">作品管理</router-link>
  </div>
  <router-view/>
  <tslg_footer/>
</div>
</template>

<script>
  import Lgts_head from '../../components/body/tslg_header'
  import tslg_footer from '../../components/body/tslg_footer'
  import cookie from '../../utils/cookie'
    export default {
        name: "lgts_person",
      components:{
        Lgts_head,
        tslg_footer,
      },
      created(){
          document.body.style.overflow='auto'
      },

    }
</script>

<style lang="scss" scoped>
  @import "../../styles/variables";
  .person{

  }
  .person-top-nav{
    height: 4rem;
    display: flex;
    justify-content: center;
    align-items: center;
    font-size: $xls;
    background: #fff;

  }
  .nav-item{
    display: flex;
    justify-content: center;
    align-items: center;
    margin-right: 3rem;
    height: 100%;
    color: $f-light;
    &:hover{
      color: #4a4a4a;
    }
  }
  .router-link-active{
    border-bottom: 0.125rem solid #000;
    color: #000;
  }
</style>
