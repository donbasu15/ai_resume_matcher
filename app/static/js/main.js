// Main JavaScript for Resume Matcher Application

document.addEventListener("DOMContentLoaded", function () {
  // Initialize components
  initializeFileUpload();
  initializeForm();
  initializeTooltips();
});

function initializeFileUpload() {
  const uploadArea = document.getElementById("uploadArea");
  const fileInput = document.getElementById("resume");
  const fileInfo = document.getElementById("fileInfo");
  const fileName = document.getElementById("fileName");
  const removeFile = document.getElementById("removeFile");

  // Drag and drop functionality
  uploadArea.addEventListener("dragover", function (e) {
    e.preventDefault();
    uploadArea.classList.add("dragover");
  });

  uploadArea.addEventListener("dragleave", function (e) {
    e.preventDefault();
    uploadArea.classList.remove("dragover");
  });

  uploadArea.addEventListener("drop", function (e) {
    e.preventDefault();
    uploadArea.classList.remove("dragover");

    const files = e.dataTransfer.files;
    if (files.length > 0) {
      const file = files[0];
      if (isValidFileType(file)) {
        fileInput.files = files;
        displayFileInfo(file);
      } else {
        showAlert("Please select a valid PDF or DOCX file.", "warning");
      }
    }
  });

  // Click to upload
  uploadArea.addEventListener("click", function () {
    fileInput.click();
  });

  // File input change
  fileInput.addEventListener("change", function (e) {
    const file = e.target.files[0];
    if (file) {
      if (isValidFileType(file)) {
        displayFileInfo(file);
      } else {
        showAlert("Please select a valid PDF or DOCX file.", "warning");
        fileInput.value = "";
      }
    }
  });

  // Remove file
  removeFile.addEventListener("click", function () {
    fileInput.value = "";
    fileInfo.style.display = "none";
    uploadArea.style.display = "block";
  });

  function isValidFileType(file) {
    const validTypes = [
      "application/pdf",
      "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
    ];
    return validTypes.includes(file.type);
  }

  function displayFileInfo(file) {
    fileName.textContent = file.name;
    fileInfo.style.display = "flex";
    uploadArea.style.display = "none";
  }
}

function initializeForm() {
  const form = document.getElementById("analyzeForm");
  const submitBtn = document.getElementById("submitBtn");
  const loadingModal = new bootstrap.Modal(
    document.getElementById("loadingModal")
  );

  form.addEventListener("submit", function (e) {
    e.preventDefault();

    // Validate form
    if (!validateForm()) {
      return;
    }

    // Show loading modal
    showLoadingModal(loadingModal);

    // Submit form
    setTimeout(() => {
      form.submit();
    }, 500);
  });

  function validateForm() {
    const fileInput = document.getElementById("resume");
    const jobDescription = document.getElementById("job_description");

    if (!fileInput.files || fileInput.files.length === 0) {
      showAlert("Please select a resume file.", "warning");
      return false;
    }

    if (!jobDescription.value.trim()) {
      showAlert("Please enter a job description.", "warning");
      return false;
    }

    if (jobDescription.value.trim().length < 50) {
      showAlert(
        "Job description seems too short. Please provide a more detailed description.",
        "warning"
      );
      return false;
    }

    return true;
  }
}

function showLoadingModal(modal) {
  modal.show();

  // Simulate progress
  const progressBar = document.getElementById("progressBar");
  let progress = 0;

  const interval = setInterval(() => {
    progress += Math.random() * 20;
    if (progress > 90) progress = 90;

    progressBar.style.width = progress + "%";

    if (progress >= 90) {
      clearInterval(interval);
    }
  }, 200);
}

function initializeTooltips() {
  // Initialize Bootstrap tooltips
  var tooltipTriggerList = [].slice.call(
    document.querySelectorAll('[data-bs-toggle="tooltip"]')
  );
  var tooltipList = tooltipTriggerList.map(function (tooltipTriggerEl) {
    return new bootstrap.Tooltip(tooltipTriggerEl);
  });
}

function showAlert(message, type = "info") {
  // Create alert element
  const alertDiv = document.createElement("div");
  alertDiv.className = `alert alert-${type} alert-dismissible fade show position-fixed`;
  alertDiv.style.cssText =
    "top: 20px; right: 20px; z-index: 9999; min-width: 300px;";

  alertDiv.innerHTML = `
        <i class="fas fa-${getAlertIcon(type)} me-2"></i>
        ${message}
        <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
    `;

  document.body.appendChild(alertDiv);

  // Auto-remove after 5 seconds
  setTimeout(() => {
    if (alertDiv.parentNode) {
      alertDiv.remove();
    }
  }, 5000);
}

function getAlertIcon(type) {
  const icons = {
    success: "check-circle",
    warning: "exclamation-triangle",
    danger: "exclamation-circle",
    info: "info-circle",
  };
  return icons[type] || "info-circle";
}

// Utility functions for results page
function animateProgressBar(elementId, targetValue) {
  const element = document.getElementById(elementId);
  if (!element) return;

  let currentValue = 0;
  const increment = targetValue / 50;

  const timer = setInterval(() => {
    currentValue += increment;
    if (currentValue >= targetValue) {
      currentValue = targetValue;
      clearInterval(timer);
    }
    element.style.width = currentValue + "%";
    element.textContent = Math.round(currentValue) + "%";
  }, 20);
}

function copyToClipboard(text) {
  navigator.clipboard
    .writeText(text)
    .then(() => {
      showAlert("Copied to clipboard!", "success");
    })
    .catch(() => {
      showAlert("Failed to copy to clipboard.", "danger");
    });
}

// Chart creation functions (if needed for future enhancements)
function createSkillsChart(canvasId, data) {
  const ctx = document.getElementById(canvasId);
  if (!ctx) return;

  // This would integrate with Chart.js if added
  console.log("Chart data:", data);
}

// Export functions for global use
window.ResumeMatcherApp = {
  showAlert,
  copyToClipboard,
  animateProgressBar,
  createSkillsChart,
};

// Add smooth scrolling for anchor links
document.querySelectorAll('a[href^="#"]').forEach((anchor) => {
  anchor.addEventListener("click", function (e) {
    e.preventDefault();
    const target = document.querySelector(this.getAttribute("href"));
    if (target) {
      target.scrollIntoView({
        behavior: "smooth",
        block: "start",
      });
    }
  });
});

// Add fade-in animation to elements when they come into view
const observerOptions = {
  threshold: 0.1,
  rootMargin: "0px 0px -50px 0px",
};

const observer = new IntersectionObserver((entries) => {
  entries.forEach((entry) => {
    if (entry.isIntersecting) {
      entry.target.classList.add("fade-in-up");
      observer.unobserve(entry.target);
    }
  });
}, observerOptions);

// Observe elements with animation class
document.querySelectorAll(".animate-on-scroll").forEach((el) => {
  observer.observe(el);
});
