document.addEventListener("DOMContentLoaded", function () {
    const sidebar = document.querySelector(".sidebar");
    const hamburger = document.getElementById("hamburger");
  
    // Automatically hide sidebar on small screens
    if (window.innerWidth < 768 && sidebar) {
      sidebar.style.display = "none";
    }
  
    // Hamburger toggle
    if (hamburger) {
      hamburger.addEventListener("click", function () {
        toggleSidebar();
      });
    }
  
    // Sidebar item click logic
    const sidebarItems = document.querySelectorAll(".sidebar-menu li");
    const tables = {
      "Citizen Management": document.getElementById("citizen-table"),
      "Complaint Management": document.getElementById("complaint-table"),
      "Government Agencies": document.getElementById("service-table"),
      "Profile": document.getElementById("profile-table"),
    };
  
    sidebarItems.forEach(item => {
      item.addEventListener("click", function () {
        // Highlight active menu item
        sidebarItems.forEach(i => i.classList.remove("active"));
        this.classList.add("active");
  
        // Hide all tables
        Object.values(tables).forEach(table => {
          if (table) table.style.display = "none";
        });
  
        // Show the relevant table
        const clickedText = this.textContent.trim();
        const targetTable = tables[clickedText];
        if (targetTable) {
          targetTable.style.display = "block";
        }
      });
    });
  });
  
  // ✅ Sidebar toggle
  function toggleSidebar() {
    const sidebar = document.querySelector('.sidebar');
    if (sidebar) {
      sidebar.style.display = sidebar.style.display === 'none' ? 'block' : 'none';
    }
  }
  
  // ✅ Dropdown toggle
  function toggleDropdown(id) {
    const dropdown = document.getElementById(id);
    if (dropdown) {
      dropdown.style.display = dropdown.style.display === 'block' ? 'none' : 'block';
    }
  }
  