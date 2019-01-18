<template>
  <div class="main">
    <Lgts_head/>
    <Lgts_lunbo/>
    <main_image/>
    <tslg_footer/>
    <router-view/>
  </div>
</template>

<script>
  import Lgts_head from '../components/body/tslg_header'
  import Lgts_lunbo from './Lgts_lunbo'
  import tslg_footer from '../components/body/tslg_footer'
  import main_image from '../views/main_image'
  import animation from '../components/animation'
    export default {
      components: {
        Lgts_lunbo,
        Lgts_head,
        tslg_footer,
        main_image,
        animation
      },
      name: "Lgts_main",
    }
</script>

<style lang="scss" scoped>
  @import "../styles/variables";
 .main{
   background: $bg;
 }
</style>
