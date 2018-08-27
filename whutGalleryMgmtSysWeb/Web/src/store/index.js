import vue from 'vue'
import vuex from 'vuex'
vue.use(vuex)

import user from './modules/user'
import imageGroup from './modules/imageGroup'
import person_card from './modules/person_card'
import person_show from './modules/person_show'
import getters from './getters'

const store =new vuex.Store({
  modules:{
    user,
    imageGroup,
    person_card,
    person_show
  },
  getters
})

export default store
