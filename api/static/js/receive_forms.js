document.addEventListener('DOMContentLoaded', () => {
    const form = document.getElementById('signup-form');

    if (form) {
        form.addEventListener('submit', async (event) => {
            event.preventDefault();

            const formData = new FormData(form);
            const jsonData = {};

            formData.forEach((value, key) => {
                jsonData[key] = value;
            });

            try {
                const response = await fetch('/users/register', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify(jsonData),
                });

                if (response.ok) {
                    console.log('Form submitted successfully');
                } else {
                    console.error('Error submitting form');
                }
            } catch (error) {
                console.error('Network error:', error);
            }
        });
    }
});