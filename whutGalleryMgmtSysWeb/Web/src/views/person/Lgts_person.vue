<template>
<div class="person">
  <Lgts_head/>
  <top_image/>
  <sign v-if="show_sign"/>
  <div class="wrap" v-if="!show_sign">
    <sign_nav/>
    <div class="bottom-wrap">
      <person_nav v-if="!show_folder_content"/>
      <router-view />
    </div>
  </div>
  <tslg_footer/>
</div>
</template>

<script>
  import Lgts_head from '../../components/body/tslg_header'
  import top_image from './top_image'
  import sign_nav from './sign/sign-nav'
  import sign from'./sign/sign'
  import person_nav from './person_nav'
  import folder_content from './main_content/folder_content'
  import tslg_footer from '../../components/body/tslg_footer'
  import cookie from '../../utils/cookie'
    export default {
        name: "lgts_person",
      components:{
        Lgts_head,
        top_image,
        sign_nav,
        sign,
        folder_content,
        person_nav,
        tslg_footer,
      },
      created(){
          document.body.style.overflow='auto'
      },
      computed:{
          show_sign(){
            return this.$store.state.person_show.show_sign
          },
        show_folder_content(){
            return this.$store.state.person_show.show_folder_content
        }
      }
    }
</script>

<style scoped>
.bottom-wrap{
  min-height: 500px;
  background: #f7fafb;
  height: auto;
}
</style>
