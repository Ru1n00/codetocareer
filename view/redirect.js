function reditectToHome() {
    console.log(window.location.pathname);
    if (localStorage.getItem('token')) {
        // Redirect to the appropriate page based on the role
        const is_student = localStorage.getItem('is_student') === 'true';
        if (is_student && window.location.pathname !== '/view/student_dashboard.html') {
            window.location.href = 'student_dashboard.html';
        } else if( !is_student && window.location.pathname !== '/view/teacher_dashboard.html') {
            window.location.href = 'teacher_dashboard.html';
        }
    }
}

reditectToHome();