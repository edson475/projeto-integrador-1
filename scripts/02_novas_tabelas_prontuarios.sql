-- =========================================================
-- EXPANSÃO DO SISTEMA: PRONTUÁRIOS SUAS E ATENDIMENTOS
-- =========================================================

-- 1. TABELA DE PRONTUÁRIOS
-- Guarda-chuva da família. Relacionamento 1 para 1 com Cadastros.
CREATE TABLE prontuarios (
    id SERIAL PRIMARY KEY,
    cadastro_ref_id INTEGER UNIQUE REFERENCES cadastros(ref_id) ON DELETE CASCADE,
    tecnico_id INTEGER REFERENCES usuarios(id) ON DELETE SET NULL, -- Técnico responsável
    data_abertura DATE DEFAULT CURRENT_DATE,
    servico_vinculado VARCHAR(50), -- Ex: PAIF, SCFV, PAEFI, etc.
    motivo_procura TEXT,
    status VARCHAR(20) DEFAULT 'Ativo',
    created_at TIMESTAMP WITH TIME ZONE DEFAULT TIMEZONE('utc', NOW()),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT TIMEZONE('utc', NOW())
);

-- 2. TABELA DE ATENDIMENTOS
-- Cada contato com a família gera um registro. 1 Prontuário para N Atendimentos
CREATE TABLE atendimentos (
    id SERIAL PRIMARY KEY,
    prontuario_id INTEGER REFERENCES prontuarios(id) ON DELETE CASCADE,
    tecnico_id INTEGER REFERENCES usuarios(id) ON DELETE SET NULL,
    data_atendimento DATE DEFAULT CURRENT_DATE,
    tipo_atendimento VARCHAR(50),
    demanda VARCHAR(100),
    descricao TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT TIMEZONE('utc', NOW())
);

-- 3. TABELA DE ENCAMINHAMENTOS
-- Destinos enviados pela equipe. 1 Atendimento para N Encaminhamentos
CREATE TABLE encaminhamentos (
    id SERIAL PRIMARY KEY,
    atendimento_id INTEGER REFERENCES atendimentos(id) ON DELETE CASCADE,
    servico_destino VARCHAR(100),
    motivo TEXT,
    status VARCHAR(20) DEFAULT 'Pendente', -- Pendente / Realizado
    retorno TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT TIMEZONE('utc', NOW())
);


-- =========================================================
-- ÍNDICES PARA OTIMIZAR BUSCAS
-- =========================================================
CREATE INDEX idx_prontuarios_cadastro ON prontuarios(cadastro_ref_id);
CREATE INDEX idx_atendimentos_prontuario ON atendimentos(prontuario_id);
CREATE INDEX idx_encaminhamentos_atendimento ON encaminhamentos(atendimento_id);


-- =========================================================
-- PERMISSÕES RLS (PARA A API DO SUPABASE)
-- =========================================================
ALTER TABLE prontuarios ENABLE ROW LEVEL SECURITY;
CREATE POLICY "Acesso total a prontuarios" ON prontuarios FOR ALL USING (true) WITH CHECK (true);

ALTER TABLE atendimentos ENABLE ROW LEVEL SECURITY;
CREATE POLICY "Acesso total a atendimentos" ON atendimentos FOR ALL USING (true) WITH CHECK (true);

ALTER TABLE encaminhamentos ENABLE ROW LEVEL SECURITY;
CREATE POLICY "Acesso total a encaminhamentos" ON encaminhamentos FOR ALL USING (true) WITH CHECK (true);
