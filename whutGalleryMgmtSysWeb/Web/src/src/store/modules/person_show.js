const person_show={
  state:{
    show_sign:false,
    show_folder_content:false
  },
  mutations:{
    SET_SHOW_SIGN:(state)=>{
      state.show_sign=!state.show_sign
    },
    SET_SHOW_FOLDER_CONTENT:(state)=>{
      state.show_folder_content=!state.show_folder_content
    }
  }
}
export default person_show
