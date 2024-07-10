<template>
  <div class="container">
    <div class="result-control">
      <h1>Blind Spot Detection System</h1>
      <div class="camera-feed">
        <label>Camera Feed</label>
        <img v-if="cameraFeedUrl" :src="cameraFeedUrl" alt="Camera Feed"/>
      </div>
      <div class="status-row">
        <div class="status-item">
          <p class="status-title">Obstacle Distance</p>
          <p class="status-value">{{ distance }} cm</p>
        </div>
        <div class="status-item">
          <p class="status-title">Accident Probability</p>
          <p class="status-value">{{ accident_probability }} %</p>
        </div>
        <div class="status-item">
          <p class="status-title">System Status</p>
          <p class="status-value">{{ system_status }}</p>
        </div>
      </div>
      <div class="lock-controls">
        <button @click="lockCar">Lock Car</button>
        <button @click="unlockCar">Unlock Car</button>
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
          <label for="accident_probability">Accident Probability:</label>
          <input type="number" v-model="input_accident_probability" id="accident_probability" />
          <button type="submit">Submit Accident Probability</button>
        </div>
      </form>
      <form @submit.prevent="sendSystemStatus">
        <div class="form-group">
          <label for="system_status">System Status:</label>
          <select v-model="input_system_status" id="system_status">
            <option value="Stage 0">Stage 0</option>
            <option value="Stage 1">Stage 1</option>
            <option value="Stage 2">Stage 2</option>
            <option value="Stage 3">Stage 3</option>
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
      input_accident_probability: '',
      input_system_status: '',
      distance: '',
      accident_probability: '',
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
        const res = await axios.post('http://127.0.0.1:5001/api/accident_probability', {
          accident_probability: this.input_accident_probability
        });
        this.response = res.data;
        this.accident_probability = this.input_accident_probability;
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
    }
  },
  mounted() {
    this.cameraFeedUrl = 'http://127.0.0.1:5001/api/video_feed';
  }
};
</script>
