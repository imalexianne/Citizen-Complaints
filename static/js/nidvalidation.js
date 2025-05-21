
    async function fetchUserData() {
        const formData = new FormData();
        formData.append("national_id", localStorage.getItem("national_id"));
    
        const response = await fetch("/verify_nid", {
            method: "POST",
            body: formData,
            headers: {
                "X-CSRFToken": "{{ csrf_token }}",
            }
        });
    
        const data = await response.json();
        if (data.name) {
            window.location.href = `'/medical_step'?name=${encodeURIComponent(data.name)}`;
        }
    }

    