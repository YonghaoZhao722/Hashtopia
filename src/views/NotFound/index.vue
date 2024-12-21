<template>
  <div class="not-found-container">
    <div class="not-found-content">
      <div class="icon-wrapper">
        <img src="../../assets/notfound.png" alt="404 Not Found" class="notfound-icon" />
      </div>
      
      <h1 class="title">Hmm...this page doesn’t exist. Try searching for something else.</h1>
      <router-link to="/" class="return-button">
        Back to Hashtopia
      </router-link>
    </div>
  </div>
</template>

<style scoped>
.not-found-container {
  min-height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 1rem;
  background-color: #f5f5f5;
}

.not-found-content {
  text-align: center;
  max-width: 400px;
  width: 100%;
  padding: 2rem;
}

.icon-wrapper {
  background-color: #f5f5f5;
  width: 120px;
  height: 120px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  margin: 0 auto 2rem;
}

.notfound-icon {
  min-width: 64px;
  width: 10vw;
  height: auto;

  object-fit: contain;
}

.title {
  font-size: 16px;
  margin-top: -1rem;
  color: #333;
  margin-bottom: 1rem;
  font-weight: 500;
}

.return-button {
  display: inline-block;
  background-color: #ff2441;
  color: white;
  padding: 0.75rem 2rem;
  border-radius: 9999px;
  text-decoration: none;
  font-weight: 500;
  transition: all 0.2s;
  opacity: 0.9;
}

.return-button:hover {
  opacity: 1;
  transform: translateY(-1px);
}

/* Responsive Design */
@media (max-width: 768px) {
  .not-found-content {
    padding: 1.5rem;
  }

  .icon-wrapper {
    width: 100px;
    height: 100px;
    margin-bottom: 1.5rem;
  }

  .title {
    font-size: 1.25rem;
  }

  .subtitle {
    font-size: 0.875rem;
    margin-bottom: 1.5rem;
  }
}

@media (max-width: 480px) {
  .not-found-content {
    padding: 1rem;
  }

  .icon-wrapper {
    width: 80px;
    height: 80px;
    margin-bottom: 1rem;
  }

  .planet-icon {
    width: 40px;
    height: 40px;
  }

  .return-button {
    padding: 0.625rem 1.5rem;
    font-size: 0.875rem;
  }
}
</style>