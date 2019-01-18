<template>
  <div class="ranking-list">
    <person_card :person_list="list" :page_nums="page_nums"/>
    <page_choice @cur_page="Page" :page_nums="page_nums"/>
  </div>
</template>

<script>
  import person_card from '../../components/card/person_card'
  import page_choice from '../../components/page_choice'
    export default {
      name: "rankingList",
      components: {page_choice,person_card},
      computed:{
        list(){
          return this.$store.state.person_card.rank_list
        },
        page_nums(){
          return Math.ceil(this.$store.state.person_card.rank_counts/4)
        }
      },
      created(){
        this.$store.dispatch('GetRankList',1)
      },
      methods: {
        Page(cur_page){
          this.$store.commit('SET_RANK_LIST_EMPTY')
          this.$store.dispatch('GetRankList',`${cur_page}`)
        }
      }
    }
</script>

<style scoped>

</style>
