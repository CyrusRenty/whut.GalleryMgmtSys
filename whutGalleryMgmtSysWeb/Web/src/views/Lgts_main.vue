<template>
  <div class="main">
    <Lgts_head/>
    <!--<main_search/>-->
    <Lgts_lunbo/>
    <!--<lgts_nav/>-->
    <!--<Lgts_image/>-->
    <main_image/>
    <tslg_footer/>
    <!--<animation/>-->
    <router-view/>
  </div>
</template>

<script>
  import lgts_nav from './lgts_nav'
  import Lgts_head from '../components/body/tslg_header'
  import Lgts_lunbo from './Lgts_lunbo'
  import Lgts_image from '../components/card/main_image_card'
  import tslg_footer from '../components/body/tslg_footer'
  import main_search from '../components/main_search'
  import main_image from '../views/main_image'
  import animation from '../components/animation'
    export default {
      components: {
        Lgts_lunbo,
        Lgts_head,
        lgts_nav,
        Lgts_image,
        tslg_footer,
        main_search,
        main_image,
        animation
      },
      name: "Lgts_main",
      created(){
      },
     computed:{

     }
    }
</script>

<style lang="scss" scoped>
  @import "../styles/variables";
 .main{
   background: $bg;
 }
</style>
