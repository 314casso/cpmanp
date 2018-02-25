<template>
  <div>    
    <v-select v-model="selected" :options="options" :filterable="false" @search="onSearch">
        <template slot="option" slot-scope="option">
            <div class="d-center">            
            {{ option.full_name }}
            </div>
        </template>
        <template slot="selected-option" scope="option">
            <div class="selected d-center">
                <img :src='option.owner.avatar_url'/> 
                {{ option.full_name }}
            </div>
        </template>
    </v-select>
  </div>
</template>

<script>
import _ from 'lodash'

export default {
  data () {
    return {
      options: [],
      selected: null
    }
  },
  methods: {
    onSearch (search, loading) {
      loading(true)
      this.search(loading, search, this)
    },
    search: _.debounce((loading, search, vm) => {
      fetch(
        `https://api.github.com/search/repositories?q=${escape(search)}`
      ).then(res => {
        res.json().then(json => (vm.options = json.items))
        loading(false)
      })
    }, 500)
  }
}
</script>