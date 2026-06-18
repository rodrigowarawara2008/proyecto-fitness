// ============================================
// SCRIPT.JS - Funcionalidades generales
// ============================================

// Esperar a que el DOM esté listo
document.addEventListener('DOMContentLoaded', function() {
    
    // ============================================
    // 1. AUTO-CERRAR ALERTAS DESPUÉS DE 5 SEGUNDOS
    // ============================================
    const alertas = document.querySelectorAll('.alert');
    alertas.forEach(function(alerta) {
        setTimeout(function() {
            const closeButton = alerta.querySelector('.btn-close');
            if (closeButton) {
                closeButton.click();
            } else {
                alerta.style.transition = 'opacity 0.5s';
                alerta.style.opacity = '0';
                setTimeout(function() {
                    alerta.remove();
                }, 500);
            }
        }, 5000);
    });
    
    // ============================================
    // 2. VALIDACIÓN DE CONTRASEÑA EN REGISTRO
    // ============================================
    const formRegistro = document.querySelector('form[action*="registro"]');
    if (formRegistro) {
        formRegistro.addEventListener('submit', function(e) {
            const password = this.querySelector('input[name="password"]');
            const confirmPassword = this.querySelector('input[name="confirm_password"]');
            
            if (password && confirmPassword) {
                if (password.value !== confirmPassword.value) {
                    e.preventDefault();
                    mostrarAlerta('Las contraseñas no coinciden', 'danger');
                    confirmPassword.classList.add('is-invalid');
                } else {
                    confirmPassword.classList.remove('is-invalid');
                }
            }
        });
        
        // Quitar la clase de error al escribir
        const confirmInput = formRegistro.querySelector('input[name="confirm_password"]');
        if (confirmInput) {
            confirmInput.addEventListener('input', function() {
                const password = document.querySelector('input[name="password"]');
                if (this.value === password.value) {
                    this.classList.remove('is-invalid');
                    this.classList.add('is-valid');
                } else {
                    this.classList.remove('is-valid');
                    this.classList.add('is-invalid');
                }
            });
        }
    }
    
    // ============================================
    // 3. MOSTRAR/OCULTAR CONTRASEÑA
    // ============================================
    const togglePasswordButtons = document.querySelectorAll('.toggle-password');
    togglePasswordButtons.forEach(function(button) {
        button.addEventListener('click', function() {
            const input = this.closest('.input-group-icon').querySelector('input');
            const icon = this.querySelector('i');
            
            if (input.type === 'password') {
                input.type = 'text';
                icon.classList.remove('fa-eye');
                icon.classList.add('fa-eye-slash');
            } else {
                input.type = 'password';
                icon.classList.remove('fa-eye-slash');
                icon.classList.add('fa-eye');
            }
        });
    });
    
    // ============================================
    // 4. CONFIRMACIÓN PARA ELIMINAR (admin)
    // ============================================
    const botonesEliminar = document.querySelectorAll('.btn-eliminar');
    botonesEliminar.forEach(function(btn) {
        btn.addEventListener('click', function(e) {
            if (!confirm('¿Estás seguro de que quieres eliminar este elemento?')) {
                e.preventDefault();
            }
        });
    });
    
    // ============================================
    // 5. ANIMACIONES AL HACER SCROLL
    // ============================================
    const elementosAnimados = document.querySelectorAll('.fade-in-up');
    
    const observer = new IntersectionObserver(function(entries) {
        entries.forEach(function(entry) {
            if (entry.isIntersecting) {
                entry.target.style.opacity = '1';
                entry.target.style.transform = 'translateY(0)';
            }
        });
    }, { threshold: 0.1 });
    
    elementosAnimados.forEach(function(el) {
        el.style.opacity = '0';
        el.style.transform = 'translateY(30px)';
        el.style.transition = 'opacity 0.6s ease, transform 0.6s ease';
        observer.observe(el);
    });
    
    // ============================================
    // 6. FUNCIÓN PARA MOSTRAR ALERTAS PERSONALIZADAS
    // ============================================
    function mostrarAlerta(mensaje, tipo) {
        const alertaExistente = document.querySelector('.alert-custom');
        if (alertaExistente) {
            alertaExistente.remove();
        }
        
        const alerta = document.createElement('div');
        alerta.className = `alert alert-modern alert-${tipo} alert-custom fade-in-up`;
        alerta.role = 'alert';
        alerta.innerHTML = `
            <i class="fas fa-${tipo === 'success' ? 'check-circle' : 'exclamation-circle'} me-2"></i>
            ${mensaje}
            <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
        `;
        
        const container = document.querySelector('main .container');
        if (container) {
            container.insertBefore(alerta, container.firstChild);
        }
        
        // Auto-cerrar después de 5 segundos
        setTimeout(function() {
            const closeButton = alerta.querySelector('.btn-close');
            if (closeButton) {
                closeButton.click();
            }
        }, 5000);
    }
    
    // ============================================
    // 7. CONTADOR DE CARACTERES EN TEXTAREA (opcional)
    // ============================================
    const textareas = document.querySelectorAll('textarea[maxlength]');
    textareas.forEach(function(textarea) {
        const contador = document.createElement('small');
        contador.className = 'text-muted float-end';
        contador.textContent = `0 / ${textarea.maxLength}`;
        textarea.parentNode.appendChild(contador);
        
        textarea.addEventListener('input', function() {
            const actual = this.value.length;
            contador.textContent = `${actual} / ${this.maxLength}`;
            
            if (actual > this.maxLength * 0.9) {
                contador.style.color = '#dc3545';
            } else {
                contador.style.color = '#6c757d';
            }
        });
    });
    
    // ============================================
    // 8. EFECTO DE CARGA EN BOTONES
    // ============================================
    const formularios = document.querySelectorAll('form');
    formularios.forEach(function(form) {
        form.addEventListener('submit', function() {
            const botones = this.querySelectorAll('button[type="submit"]');
            botones.forEach(function(btn) {
                const textoOriginal = btn.innerHTML;
                btn.disabled = true;
                btn.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Cargando...';
                
                // Restaurar después de 10 segundos (por si algo falla)
                setTimeout(function() {
                    btn.disabled = false;
                    btn.innerHTML = textoOriginal;
                }, 10000);
            });
        });
    });
    
    console.log('✅ Script.js cargado correctamente');
});