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
          <p class="status-title">Obstacle Type</p>
          <p class="status-value">{{ obstacle_type }}</p>
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
        <div class="control-modules">
          <div class="lock-controls">
            <p>Lock / Unlock</p>
            <input type="checkbox" checked="checked" id="lock" @click="toggleLock">
            <label for="lock" class="toggle-container">
              <div class="action">
                <span class="option-1">Locked</span>
                <span class="option-2">Unlocked</span>
              </div>
            </label>
          </div>
          <div class="door-controls">
            <p>Open / Close</p>
            <input type="checkbox" checked="checked" id="door" @click="toggleDoor">
            <label for="door" class="toggle-container">
              <div class="action">
                <span class="option-1">Opened</span>
                <span class="option-2">Closed</span>
              </div>
            </label>
          </div>
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
          <label for="obstacle_type">Obstacle Type:</label>
          <select v-model="input_obstacle_type" id="obstacle_type">
            <option value="Car">Car</option>
            <option value="Pedestrian">Pedestrian</option>
          </select>
          <button type="submit">Submit Obstacle Type</button>
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
      input_obstacle_type: '',
      input_system_status: '',
      distance: '',
      obstacle_type: '',
      system_status: '',
      response: null,
      cameraFeedUrl: 'http://127.0.0.1:5001/api/video_feed',
      isLocked: true, // 初始化为锁定状态
      isDoorOpen: false // 初始化为关闭状态
    };
  },
  methods: {
    async fetchData() {
      try {
        const res = await axios.get('http://127.0.0.1:5001/api/current_data');
        const data = res.data;
        this.distance = data.ultra_sonic_distance;
        this.obstacle_type = data.obstacle_type;
        this.system_status = data.system_status;
        this.cameraFeedUrl = 'http://127.0.0.1:5001/api/video_feed';
      } catch (error) {
        console.error(error);
      }
    },
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
        const res = await axios.post('http://127.0.0.1:5001/api/obstacle_type', {
          obstacle_type: this.input_obstacle_type
        });
        this.response = res.data;
        this.obstacle_type = this.input_obstacle_type;
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
        this.isLocked = true; // 更新前端锁定状态
      } catch (error) {
        console.error(error);
      }
    },
    async unlockCar() {
      try {
        const res = await axios.post('http://127.0.0.1:5001/api/unlock');
        this.response = res.data;
        this.isLocked = false; // 更新前端锁定状态
      } catch (error) {
        console.error(error);
      }
    },
    async openDoor() {
      try {
        const res = await axios.post('http://127.0.0.1:5001/api/open');
        this.response = res.data;
        this.isDoorOpen = true; // 更新前端开门状态
      } catch (error) {
        console.error(error);
        this.isDoorOpen = false; // 如果请求失败，保持关门状态
      }
    },
    async closeDoor() {
      try {
        const res = await axios.post('http://127.0.0.1:5001/api/close');
        this.response = res.data;
        this.isDoorOpen = false; // 更新前端关门状态
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
    },
    toggleDoor(event) {
      if (this.isLocked) {
        // 如果车辆是锁定状态，阻止切换
        event.preventDefault();
        return;
      }
      if (event.target.checked) {
        this.closeDoor();
      } else {
        this.openDoor();
      }
    }
  },
  mounted() {
    // this.cameraFeedUrl = 'http://127.0.0.1:5001/api/video_feed';
    this.fetchData();
    setInterval(this.fetchData, 5000);
  }
};
</script>
