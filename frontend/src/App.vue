<template>
  <div id="app">
    <BlindSpotDetection />
  </div>
</template>

<script>
import BlindSpotDetection from './components/BlindSpotDetection.vue';

export default {
  name: 'App',
  components: {
    BlindSpotDetection
  }
};
</script>

<style>
html, body {
  height: 100%;
  margin: 0;
}

#app {
  height: 100%;
  display: flex;
  flex-direction: column;
}
</style>
