/**
 * Sistema de Cadastro de Assistência Social
 * JavaScript Principal
 */

// =====================================================
// FUNÇÕES GERAIS
// =====================================================

/**
 * Formata CPF
 */
function formatarCPF(valor) {
    let cpf = valor.replace(/\D/g, '');
    if (cpf.length <= 11) {
        cpf = cpf.replace(/(\d{3})(\d)/, '$1.$2');
        cpf = cpf.replace(/(\d{3})(\d)/, '$1.$2');
        cpf = cpf.replace(/(\d{3})(\d{1,2})$/, '$1-$2');
    }
    return cpf;
}

/**
 * Formata NIS
 */
function formatarNIS(valor) {
    let nis = valor.replace(/\D/g, '');
    if (nis.length <= 11) {
        nis = nis.replace(/(\d{3})(\d)/, '$1.$2');
        nis = nis.replace(/(\d{5})(\d)/, '$1.$2');
        nis = nis.replace(/(\d{2})(\d{1,2})$/, '$1-$2');
    }
    return nis;
}

/**
 * Formata CEP
 */
function formatarCEP(valor) {
    let cep = valor.replace(/\D/g, '');
    if (cep.length <= 8) {
        cep = cep.replace(/(\d{5})(\d)/, '$1-$2');
    }
    return cep;
}

/**
 * Formata Telefone
 */
function formatarTelefone(valor) {
    let tel = valor.replace(/\D/g, '');
    if (tel.length <= 11) {
        tel = tel.replace(/(\d{2})(\d)/, '($1) $2');
        tel = tel.replace(/(\d{5})(\d)/, '$1-$2');
    }
    return tel;
}

/**
 * Formata Data (DD/MM/YYYY)
 */
function formatarData(valor) {
    let data = valor.replace(/\D/g, '');
    if (data.length <= 10) {
        data = data.replace(/(\d{2})(\d)/, '$1/$2');
        data = data.replace(/(\d{2})(\d)/, '$1/$2');
    }
    return data;
}

/**
 * Valida CPF (algoritmo básico)
 */
function validarCPF(cpf) {
    cpf = cpf.replace(/\D/g, '');
    
    if (cpf.length !== 11) return false;
    
    // Verifica se todos os dígitos são iguais
    if (/^(\d)\1+$/.test(cpf)) return false;
    
    // Validação dos dígitos verificadores
    let soma = 0;
    let resto;
    
    for (let i = 1; i <= 9; i++) {
        soma += parseInt(cpf.substring(i - 1, i)) * (11 - i);
    }
    
    resto = (soma * 10) % 11;
    if (resto === 10 || resto === 11) resto = 0;
    
    if (resto !== parseInt(cpf.substring(9, 10))) return false;
    
    soma = 0;
    for (let i = 1; i <= 10; i++) {
        soma += parseInt(cpf.substring(i - 1, i)) * (12 - i);
    }
    
    resto = (soma * 10) % 11;
    if (resto === 10 || resto === 11) resto = 0;
    
    if (resto !== parseInt(cpf.substring(10, 11))) return false;
    
    return true;
}

// =====================================================
// INICIALIZAÇÃO
// =====================================================

document.addEventListener('DOMContentLoaded', function() {
    
    // Aplicar máscaras em todos os campos relevantes
    const camposCPF = document.querySelectorAll('input[name="cpf"]');
    camposCPF.forEach(input => {
        input.addEventListener('input', function(e) {
            e.target.value = formatarCPF(e.target.value);
        });
    });
    
    const camposNIS = document.querySelectorAll('input[name="nis"]');
    camposNIS.forEach(input => {
        input.addEventListener('input', function(e) {
            e.target.value = formatarNIS(e.target.value);
        });
    });
    
    const camposCEP = document.querySelectorAll('input[name="cep"]');
    camposCEP.forEach(input => {
        input.addEventListener('input', function(e) {
            e.target.value = formatarCEP(e.target.value);
        });
    });
    
    const camposTelefone = document.querySelectorAll('input[name="telefone"]');
    camposTelefone.forEach(input => {
        input.addEventListener('input', function(e) {
            e.target.value = formatarTelefone(e.target.value);
        });
    });
    
    const camposData = document.querySelectorAll('input[name="data_nascimento"]');
    camposData.forEach(input => {
        input.addEventListener('input', function(e) {
            e.target.value = formatarData(e.target.value);
        });
    });
    
    // Auto-fechar alerts após 5 segundos
    const alerts = document.querySelectorAll('.alert-dismissible');
    alerts.forEach(alert => {
        setTimeout(() => {
            const bsAlert = new bootstrap.Alert(alert);
            bsAlert.close();
        }, 5000);
    });
    
    // Confirmação de exclusão
    const formsExclusao = document.querySelectorAll('form[onsubmit*="confirm"]');
    formsExclusao.forEach(form => {
        form.addEventListener('submit', function(e) {
            if (!confirm('Tem certeza que deseja continuar?')) {
                e.preventDefault();
            }
        });
    });
    
    console.log('Sistema de Cadastro inicializado com sucesso!');
});

// =====================================================
// FUNÇÕES DE UTILIDADE
// =====================================================

/**
 * Mostra um toast/notificação
 */
function mostrarToast(mensagem, tipo = 'info') {
    const toastContainer = document.querySelector('.toast-container');
    
    if (!toastContainer) {
        const container = document.createElement('div');
        container.className = 'toast-container position-fixed bottom-0 end-0 p-3';
        document.body.appendChild(container);
    }
    
    const toast = document.createElement('div');
    toast.className = `toast align-items-center text-white bg-${tipo} border-0`;
    toast.setAttribute('role', 'alert');
    toast.innerHTML = `
        <div class="d-flex">
            <div class="toast-body">${mensagem}</div>
            <button type="button" class="btn-close btn-close-white me-2 m-auto" data-bs-dismiss="toast"></button>
        </div>
    `;
    
    document.querySelector('.toast-container').appendChild(toast);
    
    const bsToast = new bootstrap.Toast(toast);
    bsToast.show();
    
    toast.addEventListener('hidden.bs.toast', () => {
        toast.remove();
    });
}

/**
 * Faz download de um arquivo
 */
function downloadArquivo(conteudo, nomeArquivo, tipo = 'text/plain') {
    const elemento = document.createElement('a');
    elemento.setAttribute('href', 'data:' + tipo + ';charset=utf-8,' + encodeURIComponent(conteudo));
    elemento.setAttribute('download', nomeArquivo);
    elemento.style.display = 'none';
    document.body.appendChild(elemento);
    elemento.click();
    document.body.removeChild(elemento);
}
