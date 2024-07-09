<template>
  <BlindSpotDetection />
</template>

<script>
import BlindSpotDetection from './components/BlindSpotDetection.vue'

export default {
  name: 'App',
  components: {
    BlindSpotDetection
  }
}
</script>

<style>
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  margin-top: 60px;
}
</style>
