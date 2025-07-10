// OSIRIS Login - Efectos Interactivos
document.addEventListener('DOMContentLoaded', function() {
    
    // Efecto de escritura automática
    const texts = [
        "Agenda tus citas médicas",
        "Mantente al día con tu salud",
        "Conecta con especialistas",
        "Gestión médica inteligente"
    ];
    
    const multipleText = document.querySelector('.multiple-text');
    if (multipleText) {
        let textIndex = 0;
        let charIndex = 0;
        let isDeleting = false;
        
        function typeEffect() {
            const currentText = texts[textIndex];
            
            if (isDeleting) {
                multipleText.textContent = currentText.substring(0, charIndex - 1);
                charIndex--;
            } else {
                multipleText.textContent = currentText.substring(0, charIndex + 1);
                charIndex++;
            }
            
            let typeSpeed = 100;
            
            if (isDeleting) {
                typeSpeed = 50;
            }
            
            if (!isDeleting && charIndex === currentText.length) {
                typeSpeed = 2000;
                isDeleting = true;
            } else if (isDeleting && charIndex === 0) {
                isDeleting = false;
                textIndex = (textIndex + 1) % texts.length;
                typeSpeed = 500;
            }
            
            setTimeout(typeEffect, typeSpeed);
        }
        
        typeEffect();
    }
    
    // Efecto de parallax suave en el fondo
    document.addEventListener('mousemove', function(e) {
        const mouseX = e.clientX / window.innerWidth;
        const mouseY = e.clientY / window.innerHeight;
        
        const loginContainer = document.querySelector('.login-container');
        if (loginContainer) {
            loginContainer.style.transform = `translate(${mouseX * 10}px, ${mouseY * 10}px)`;
        }
    });
    
    // Efecto de ondas al hacer clic
    function createRipple(event) {
        const button = event.currentTarget;
        const circle = document.createElement('span');
        const diameter = Math.max(button.clientWidth, button.clientHeight);
        const radius = diameter / 2;
        
        circle.style.width = circle.style.height = `${diameter}px`;
        circle.style.left = `${event.clientX - button.offsetLeft - radius}px`;
        circle.style.top = `${event.clientY - button.offsetTop - radius}px`;
        circle.classList.add('ripple');
        
        const ripple = button.getElementsByClassName('ripple')[0];
        if (ripple) {
            ripple.remove();
        }
        
        button.appendChild(circle);
    }
    
    // Añadir efecto de ondas a botones
    const buttons = document.querySelectorAll('.btn-login');
    buttons.forEach(button => {
        button.addEventListener('click', createRipple);
        button.style.position = 'relative';
        button.style.overflow = 'hidden';
    });
    
    // Validación visual en tiempo real
    const inputs = document.querySelectorAll('.form-group input');
    inputs.forEach(input => {
        input.addEventListener('input', function() {
            if (this.value.length > 0) {
                this.style.borderColor = '#0ef';
                this.style.boxShadow = '0 0 10px rgba(0, 238, 255, 0.3)';
            } else {
                this.style.borderColor = 'rgba(0, 238, 255, 0.3)';
                this.style.boxShadow = 'none';
            }
        });
        
        input.addEventListener('focus', function() {
            this.parentElement.style.transform = 'translateY(-2px)';
        });
        
        input.addEventListener('blur', function() {
            this.parentElement.style.transform = 'translateY(0)';
        });
    });
    
    // Efecto de carga suave
    const fadeElements = document.querySelectorAll('.login-form, .login-content, .login-image');
    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.style.opacity = '1';
                entry.target.style.transform = 'translateY(0)';
            }
        });
    });
    
    fadeElements.forEach(element => {
        observer.observe(element);
    });
    
    // Partículas flotantes de fondo
    function createFloatingParticles() {
        const particlesContainer = document.createElement('div');
        particlesContainer.className = 'particles-container';
        particlesContainer.style.cssText = `
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            pointer-events: none;
            z-index: 0;
        `;
        
        document.body.appendChild(particlesContainer);
        
        for (let i = 0; i < 20; i++) {
            const particle = document.createElement('div');
            particle.className = 'particle';
            particle.style.cssText = `
                position: absolute;
                width: 4px;
                height: 4px;
                background: rgba(0, 238, 255, 0.5);
                border-radius: 50%;
                animation: float ${5 + Math.random() * 5}s ease-in-out infinite;
                left: ${Math.random() * 100}%;
                top: ${Math.random() * 100}%;
                animation-delay: ${Math.random() * 5}s;
            `;
            particlesContainer.appendChild(particle);
        }
    }
    
    // Crear partículas flotantes
    createFloatingParticles();
    
    // Añadir animación CSS para partículas
    const style = document.createElement('style');
    style.textContent = `
        @keyframes float {
            0%, 100% { transform: translateY(0px) rotate(0deg); }
            33% { transform: translateY(-20px) rotate(120deg); }
            66% { transform: translateY(10px) rotate(240deg); }
        }
        
        .ripple {
            position: absolute;
            border-radius: 50%;
            background: rgba(255, 255, 255, 0.3);
            transform: scale(0);
            animation: ripple-animation 0.6s linear;
        }
        
        @keyframes ripple-animation {
            to {
                transform: scale(4);
                opacity: 0;
            }
        }
    `;
    document.head.appendChild(style);
    
    // Efectos de sonido (opcional)
    function playSound(type) {
        // Aquí podrías añadir efectos de sonido si lo deseas
        // const audio = new Audio(`/static/sounds/${type}.mp3`);
        // audio.play();
    }
    
    // Detección de tecla Enter para enviar formulario
    document.addEventListener('keypress', function(e) {
        if (e.key === 'Enter') {
            const loginForm = document.querySelector('.login-form form');
            if (loginForm && document.activeElement.tagName === 'INPUT') {
                loginForm.submit();
            }
        }
    });
    
    // Mensaje de bienvenida personalizado según la hora
    const welcomeMessage = document.querySelector('.welcome-message');
    if (welcomeMessage) {
        const hour = new Date().getHours();
        let greeting;
        
        if (hour < 12) {
            greeting = "Buenos días";
        } else if (hour < 18) {
            greeting = "Buenas tardes";
        } else {
            greeting = "Buenas noches";
        }
        
        welcomeMessage.textContent = `${greeting}, bienvenido a OSIRIS`;
    }
});