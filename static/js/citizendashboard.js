document.addEventListener("DOMContentLoaded", function () {
    const sidebarItems = document.querySelectorAll(".sidebar-menu li");
    const citizenTable = document.getElementById("citizen-table");
    const complaintTable = document.getElementById("complaint-table");
    const serviceTable = document.getElementById("service-table");
    const profileTable = document.getElementById("profile-table");
  
    sidebarItems.forEach(item => {
      item.addEventListener("click", function () {
        sidebarItems.forEach(i => i.classList.remove("active"));
        this.classList.add("active");
  
        const text = this.textContent.trim();
  
        citizenTable.style.display = text === "Dashboard" ? "block" : "none";
        complaintTable.style.display = text === "Complaint Management" ? "block" : "none";
        serviceTable.style.display = text === "Government Agencies" ? "block" : "none";
        profileTable.style.display = text === "Profile" ? "block" : "none";
      });
    });
  
    // Optional: Hide sidebar on small screens by default
    const sidebar = document.querySelector('.sidebar');
    if (window.innerWidth < 768) {
      sidebar.style.display = 'none';
    }
  
    const hamburger = document.getElementById('hamburger');
    if (hamburger) {
      hamburger.addEventListener('click', () => {
        sidebar.classList.toggle('visible');
      });
    }
  });
  