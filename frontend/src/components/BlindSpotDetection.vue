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
          <p class="status-value">{{ getSystemStatusText(system_status) }}</p>
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
            <input type="checkbox" :checked="lock_status === 2" id="lock" @change="toggleLock">
            <label for="lock" class="toggle-container">
              <div class="action">
                <span class="option-1">Unlocked</span>
                <span class="option-2">Locked</span>
              </div>
            </label>
          </div>
          <div class="door-controls">
            <p>Open / Close</p>
            <input type="checkbox" :checked="door_status === 2" id="door" @change="toggleDoor">
            <label for="door" class="toggle-container">
              <div class="action">
                <span class="option-1">Closed</span>
                <span class="option-2">Opened</span>
              </div>
            </label>
          </div>
        </div>
      </div>
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
      lock_status: 2, // 1: unlocked, 2: locked
      door_status: 1, // 1: closed, 2: open
      response: null,
      cameraFeedUrl: 'http://127.0.0.1:5001/api/video_feed'
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
        this.lock_status = data.lock_status;
        this.door_status = data.door_status;
        this.cameraFeedUrl = 'http://127.0.0.1:5001/api/video_feed';
      } catch (error) {
        console.error(error);
      }
    },
    getSystemStatusText(status) {
      switch(status) {
        case 1:
          return 'Safe';
        case 2:
          return 'Warning';
        case 3:
          return 'Dangerous';
        default:
          return 'Unknown';
      }
    },
    async sendDistance() {
      try {
        const res = await axios.post('http://127.0.0.1:5001/api/ultra_sonic_distance', {
          ultra_sonic_distance: this.input_distance
        });
        this.response = res.data;
      } catch (error) {
        console.error(error);
      }
    },
    async sendObstacleType() {
      try {
        const res = await axios.post('http://127.0.0.1:5001/api/obstacle_type', {
          obstacle_type: this.input_obstacle_type
        });
        this.response = res.data;
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
    async openDoor() {
      try {
        const res = await axios.post('http://127.0.0.1:5001/api/open');
        this.response = res.data;
      } catch (error) {
        console.error(error);
      }
    },
    async closeDoor() {
      try {
        const res = await axios.post('http://127.0.0.1:5001/api/close');
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
    },
    toggleDoor(event) {
      if (event.target.checked) {
        this.openDoor();
      } else {
        this.closeDoor();
      }
    }
  },
  mounted() {
    this.fetchData();
    setInterval(this.fetchData, 500);
  }
};
</script>
