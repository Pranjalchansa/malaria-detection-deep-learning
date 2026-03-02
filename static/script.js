// ================= LOAD USERS =================
let users = JSON.parse(localStorage.getItem("users")) || {};

// ================= PAGE SWITCH =================
function switchPage(id) {
  document.querySelectorAll(".page").forEach((p) => {
    p.classList.remove("active");
  });

  const page = document.getElementById(id);
  if (page) {
    page.classList.add("active");
  }
}

function showSignup() {
  switchPage("signupPage");
}
function showLogin() {
  switchPage("loginPage");
}
function showHome() {
  switchPage("homePage");
}
function showUpload() {
  switchPage("uploadPage");
}
function logout() {
  switchPage("loginPage");
}

// ================= DOM READY =================
document.addEventListener("DOMContentLoaded", function () {
  // 🔹 Signup Navigation
  const goSignup = document.getElementById("goSignup");
  if (goSignup) {
    goSignup.addEventListener("click", function () {
      switchPage("signupPage");
    });
  }

  // 🔹 Login Navigation
  const goLogin = document.getElementById("goLogin");
  if (goLogin) {
    goLogin.addEventListener("click", function () {
      switchPage("loginPage");
    });
  }

  // ================= SIGNUP =================
  const signupBtn = document.getElementById("signupBtn");
  if (signupBtn) {
    signupBtn.addEventListener("click", function () {
      const user = document.getElementById("signupUser").value.trim();
      const pass = document.getElementById("signupPass").value.trim();

      if (!user || !pass) {
        alert("Please fill all fields");
        return;
      }

      if (users[user]) {
        alert("User already exists");
        return;
      }

      users[user] = pass;
      localStorage.setItem("users", JSON.stringify(users));

      alert("Account Created Successfully ✅");

      document.getElementById("signupUser").value = "";
      document.getElementById("signupPass").value = "";

      switchPage("loginPage");
    });
  }

  // ================= LOGIN =================
  const loginBtn = document.getElementById("loginBtn");
  if (loginBtn) {
    loginBtn.addEventListener("click", function () {
      const user = document.getElementById("loginUser").value.trim();
      const pass = document.getElementById("loginPass").value.trim();

      if (users[user] === pass) {
        switchPage("homePage");
      } else {
        alert("Invalid Credentials ❌");
      }
    });
  }

  // ================= IMAGE PREVIEW =================
  const imageInput = document.getElementById("imageInput");
  if (imageInput) {
    imageInput.addEventListener("change", function (event) {
      const file = event.target.files[0];
      if (file) {
        const reader = new FileReader();
        reader.onload = function (e) {
          const img = document.getElementById("preview");
          img.src = e.target.result;
          img.style.display = "block";
        };
        reader.readAsDataURL(file);
      }
    });
  }
});

// ================= DUMMY PREDICTION =================
function predict() {
  const result = document.getElementById("result");

  if (!document.getElementById("preview").src) {
    alert("Please upload an image first");
    return;
  }

  const random = Math.random();

  if (random > 0.5) {
    result.innerText = "Result: Infected 🦟";
    result.style.color = "red";
  } else {
    result.innerText = "Result: Uninfected ✅";
    result.style.color = "lightgreen";
  }
}
