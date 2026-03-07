// ================= LOAD USERS =================

let users = JSON.parse(localStorage.getItem("users")) || {};

// ================= USER SESSION =================

let currentUser = localStorage.getItem("currentUser");

// ================= PAGE SWITCH SYSTEM =================

function hideAllPages() {
  document.querySelectorAll(".page").forEach((page) => {
    page.classList.remove("active");
  });
}

function switchPage(pageId) {
  hideAllPages();

  const page = document.getElementById(pageId);

  if (page) {
    page.classList.add("active");
    window.scrollTo(0, 0);
  }
}

// ================= PAGE NAVIGATION =================

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

function showPerformance() {
  switchPage("performancePage");
}

function showTechnology() {
  switchPage("technologyPage");
}

// ================= LOGOUT =================

function logout() {
  localStorage.removeItem("currentUser");

  alert("Logged out successfully 👋");

  switchPage("loginPage");
}

// ================= DOM READY =================

document.addEventListener("DOMContentLoaded", function () {
  // ================= AUTO LOGIN =================

  if (currentUser) {
    showHome();
  }

  // ================= NAVIGATION BUTTONS =================

  const goSignup = document.getElementById("goSignup");

  if (goSignup) {
    goSignup.addEventListener("click", showSignup);
  }

  const goLogin = document.getElementById("goLogin");

  if (goLogin) {
    goLogin.addEventListener("click", showLogin);
  }

  // ================= SIGNUP =================

  const signupBtn = document.getElementById("signupBtn");

  if (signupBtn) {
    signupBtn.addEventListener("click", function () {
      const user = document.getElementById("signupUser").value.trim();
      const pass = document.getElementById("signupPass").value.trim();

      if (!user || !pass) {
        alert("Please fill all fields ⚠");

        return;
      }

      if (users[user]) {
        alert("User already exists ❌");

        return;
      }

      users[user] = pass;

      localStorage.setItem("users", JSON.stringify(users));

      alert("Account Created Successfully ✅");

      document.getElementById("signupUser").value = "";
      document.getElementById("signupPass").value = "";

      showLogin();
    });
  }

  // ================= LOGIN =================

  const loginBtn = document.getElementById("loginBtn");

  if (loginBtn) {
    loginBtn.addEventListener("click", function () {
      const user = document.getElementById("loginUser").value.trim();
      const pass = document.getElementById("loginPass").value.trim();

      if (!user || !pass) {
        alert("Please enter username and password");

        return;
      }

      if (users[user] === pass) {
        alert("Login Successful ✅");

        localStorage.setItem("currentUser", user);

        showHome();
      } else {
        alert("Invalid Credentials ❌");
      }
    });
  }

  // ================= ENTER KEY LOGIN =================

  document.addEventListener("keypress", function (e) {
    if (e.key === "Enter") {
      const loginBtn = document.getElementById("loginBtn");

      if (loginBtn) {
        loginBtn.click();
      }
    }
  });

  // ================= IMAGE PREVIEW =================

  const imageInput = document.querySelector("input[type='file']");

  if (imageInput) {
    imageInput.addEventListener("change", function (event) {
      const file = event.target.files[0];

      if (!file) return;

      let previewContainer = document.getElementById("previewContainer");
      let previewImage = document.getElementById("previewImage");

      if (!previewContainer) {
        previewContainer = document.createElement("div");

        previewContainer.id = "previewContainer";

        previewContainer.style.marginTop = "20px";

        previewImage = document.createElement("img");

        previewImage.id = "previewImage";

        previewImage.style.maxWidth = "300px";

        previewImage.style.borderRadius = "15px";

        previewContainer.appendChild(previewImage);

        imageInput.parentElement.appendChild(previewContainer);
      }

      const reader = new FileReader();

      reader.onload = function (e) {
        previewImage.src = e.target.result;
      };

      reader.readAsDataURL(file);
    });
  }

  // ================= AUTO OPEN UPLOAD PAGE AFTER PREDICTION =================

  if (document.querySelector(".result-box")) {
    showUpload();
  }
});
