const image={
  state:{
    edit_item:{}
  },
  mutations:{
    SET_EDIT_ITEM(state,data){
      console.log(data);
      state.edit_item=data
    }
  }
};
export default image
