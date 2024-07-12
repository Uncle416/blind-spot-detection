<template>
  <div class="container">
    <h1>Blind Spot Detection System</h1>
    <div class="result-control">
      <div class="status-column">
        <div class="status-item">
          <p class="status-title">Obstacle Distance</p>
          <p class="status-value">{{ distance }} cm</p>
        </div>
        <div class="status-item">
          <p class="status-title">Obstacle Speed</p>
          <p class="status-value">{{ obstacle_speed }} km/h</p>
        </div>
        <div class="status-item">
          <p class="status-title">System Status</p>
          <p class="status-value">Stage{{ system_status }}</p>
        </div>
      </div>
      <div class="camera-feed-section">
        <div class="camera-feed">
          <label>Camera Feed</label>
          <img v-if="cameraFeedUrl" :src="cameraFeedUrl" alt="Camera Feed"/>
        </div>
        <div class="lock-controls">
          <p>Lock / Unlock</p>
          <label class="toggle-container">
            <input checked="checked" type="checkbox" @click="toggleLock">
            <svg viewBox="0 0 576 512" height="1em" xmlns="http://www.w3.org/2000/svg" class="lock-open"><path d="M352 144c0-44.2 35.8-80 80-80s80 35.8 80 80v48c0 17.7 14.3 32 32 32s32-14.3 32-32V144C576 64.5 511.5 0 432 0S288 64.5 288 144v48H64c-35.3 0-64 28.7-64 64V448c0 35.3 28.7 64 64 64H384c35.3 0 64-28.7 64-64V256c0-35.3-28.7-64-64-64H352V144z"></path></svg>
            <svg viewBox="0 0 448 512" height="1em" xmlns="http://www.w3.org/2000/svg" class="lock"><path d="M144 144v48H304V144c0-44.2-35.8-80-80-80s-80 35.8-80 80zM80 192V144C80 64.5 144.5 0 224 0s144 64.5 144 144v48h16c35.3 0 64 28.7 64 64V448c0 35.3-28.7 64-64 64H64c-35.3 0-64-28.7-64-64V256c0-35.3 28.7-64 64-64H80z"></path></svg>
          </label>
        </div>
      </div>
    </div>
    <div class="input-section">
      <form @submit.prevent="sendDistance">
        <div class="form-group">
          <label for="distance">Ultra Sonic Sensor Distance:</label>
          <input type="number" v-model="input_distance" id="distance" />
          <button type="submit">Submit Distance</button>
        </div>
      </form>
      <form @submit.prevent="sendAccidentProbability">
        <div class="form-group">
          <label for="obstacle_speed">Obstacle Speed:</label>
          <input type="number" v-model="input_obstacle_speed" id="obstacle_speed" />
          <button type="submit">Submit Obstacle Speed</button>
        </div>
      </form>
      <form @submit.prevent="sendSystemStatus">
        <div class="form-group">
          <label for="system_status">System Status:</label>
          <select v-model="input_system_status" id="system_status">
            <option value=" 0">Stage 0</option>
            <option value=" 1">Stage 1</option>
            <option value=" 2">Stage 2</option>
            <option value=" 3">Stage 3</option>
          </select>
          <button type="submit">Submit System Status</button>
        </div>
      </form>
    </div>
    <div v-if="response" class="response">
      <h2>Response:</h2>
      <pre>{{ response }}</pre>
    </div>
  </div>
</template>

<script>
import axios from 'axios';
import './BlindSpotDetection.css';  // 引入新的 CSS 文件

export default {
  data() {
    return {
      input_distance: '',
      input_obstacle_speed: '',
      input_system_status: '',
      distance: '',
      obstacle_speed: '',
      system_status: '',
      response: null,
      cameraFeedUrl: 'http://127.0.0.1:5001/api/video_feed'
    };
  },
  methods: {
    async sendDistance() {
      try {
        const res = await axios.post('http://127.0.0.1:5001/api/ultra_sonic_distance', {
          ultra_sonic_distance: this.input_distance
        });
        this.response = res.data;
        this.distance = this.input_distance;
      } catch (error) {
        console.error(error);
      }
    },
    async sendAccidentProbability() {
      try {
        const res = await axios.post('http://127.0.0.1:5001/api/obstacle_speed', {
          obstacle_speed: this.input_obstacle_speed
        });
        this.response = res.data;
        this.obstacle_speed = this.input_obstacle_speed;
      } catch (error) {
        console.error(error);
      }
    },
    async sendSystemStatus() {
      try {
        const res = await axios.post('http://127.0.0.1:5001/api/system_status', {
          system_status: this.input_system_status
        });
        this.response = res.data;
        this.system_status = this.input_system_status;
      } catch (error) {
        console.error(error);
      }
    },
    async lockCar() {
      try {
        const res = await axios.post('http://127.0.0.1:5001/api/lock');
        this.response = res.data;
      } catch (error) {
        console.error(error);
      }
    },
    async unlockCar() {
      try {
        const res = await axios.post('http://127.0.0.1:5001/api/unlock');
        this.response = res.data;
      } catch (error) {
        console.error(error);
      }
    },
    toggleLock(event) {
      if (event.target.checked) {
        this.unlockCar();
      } else {
        this.lockCar();
      }
    }
  },
  mounted() {
    this.cameraFeedUrl = 'http://127.0.0.1:5001/api/video_feed';
  }
};
</script>
