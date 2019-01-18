<template>
    <div>
      <top_image/>
      <!--<sign v-if="show_sign"/>-->
      <div class="bottom-wrap">
        <div class="nav-wrap" v-if="$router.currentRoute.name!=='sign'">
          <sign_nav/>
          <person_nav v-if="this.$router.currentRoute.name!=='folder_content'"/>
        </div>
        <router-view/>
      </div>
    </div>
</template>

<script>
  import top_image from './top_image'
  import sign_nav from '../sign/sign-nav'
  import sign from'../sign/sign'
  import person_nav from './person_nav'
  import folder_content from './main_content/folder_content'
    export default {
      name: "index",
      components: {
        top_image,
        sign_nav,
        sign,
        folder_content,
        person_nav,
      },
      computed: {
        show_sign() {
          return this.$store.state.person_show.show_sign
        },
        show_folder_content() {
          return this.$store.state.person_show.show_folder_content
        }
      }
    }
</script>

<style scoped>
  .bottom-wrap{
    background: #f0f0f0;
  }
  .nav-wrap{
    background:#fff;
  }
</style>
