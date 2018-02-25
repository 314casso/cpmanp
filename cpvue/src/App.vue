<template>
  <div id="app">
    <img src="./assets/logo.png">
    <div v-if="$auth.ready()">
      <router-view></router-view>
    </div>
    <div v-if="!$auth.ready()">
      <b-container class="bv-example-row">    
        <b-row class="justify-content-md-center">           
          <cube-spin></cube-spin>
        </b-row>
      </b-container>
    </div>
  </div>
</template>

<script>
import CubeSpin from 'vue-loading-spinner/src/components/Circle10'
export default {
  components: {
    CubeSpin
  },
  name: 'app'
}
</script>

<style>
#app {
  font-family: 'Avenir', Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  margin-top: 60px;
}
</style>
