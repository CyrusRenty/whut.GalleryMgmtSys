<template>
  <div class="main">
    <Lgts_head/>
    <Lgts_lunbo/>
    <lgts_nav/>
    <Lgts_image/>
    <tslg_footer/>
    <router-view/>
  </div>
</template>

<script>
  import lgts_nav from './lgts_nav'
  import Lgts_head from '../components/body/Lgts_head'
  import Lgts_lunbo from './Lgts_lunbo'
  import Lgts_image from '../components/card/main_image_card'
  import tslg_footer from '../components/body/tslg_footer'
  import collect from '../components/card/collect'
    export default {
      components: {
        Lgts_lunbo,
        Lgts_head,
        lgts_nav,
        Lgts_image,
        tslg_footer,
        collect
      },
      name: "Lgts_main",
      created(){
      },
     computed:{

     }
    }
</script>

<style scoped>
 .main{
   background: #f7fafb;
 }
</style>
