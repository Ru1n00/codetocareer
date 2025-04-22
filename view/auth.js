function authMiddleware() {
  if(!localStorage.getItem('token')) {
    window.location.href = "index.html";
  }
}

authMiddleware();