-- =====================================================
-- SCRIPT DE CRIAÇÃO DAS TABELAS - SUPABASE
-- Sistema de Cadastro de Assistência Social
-- =====================================================

-- =====================================================
-- 1. TABELA DE CADASTROS
-- =====================================================
CREATE TABLE IF NOT EXISTS cadastros (
    id BIGSERIAL PRIMARY KEY,
    ref_id INTEGER UNIQUE NOT NULL,
    nome VARCHAR(200) NOT NULL,
    data_ref VARCHAR(20),
    nis VARCHAR(15),
    rg VARCHAR(20),
    endereco VARCHAR(200),
    numero VARCHAR(10),
    complemento VARCHAR(50),
    bairro VARCHAR(100),
    cep VARCHAR(10),
    telefone VARCHAR(20),
    cpf VARCHAR(14),
    data_nascimento VARCHAR(20),
    email VARCHAR(100),
    prioritario BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT TIMEZONE('utc', NOW()),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT TIMEZONE('utc', NOW())
);

-- =====================================================
-- 2. TABELA DE MEMBROS DA FAMÍLIA
-- =====================================================
CREATE TABLE IF NOT EXISTS membros_familia (
    id BIGSERIAL PRIMARY KEY,
    ref_id INTEGER REFERENCES cadastros(ref_id) ON DELETE CASCADE,
    nome VARCHAR(200) NOT NULL,
    data_nascimento VARCHAR(20),
    vinculo VARCHAR(50),
    titular BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT TIMEZONE('utc', NOW())
);

-- =====================================================
-- 3. ÍNDICES PARA MELHORAR PERFORMANCE
-- =====================================================

-- Índices na tabela cadastros
CREATE INDEX IF NOT EXISTS idx_cadastros_nome ON cadastros(nome);
CREATE INDEX IF NOT EXISTS idx_cadastros_cpf ON cadastros(cpf);
CREATE INDEX IF NOT EXISTS idx_cadastros_nis ON cadastros(nis);
CREATE INDEX IF NOT EXISTS idx_cadastros_ref ON cadastros(ref_id);
CREATE INDEX IF NOT EXISTS idx_cadastros_bairro ON cadastros(bairro);
CREATE INDEX IF NOT EXISTS idx_cadastros_prioritario ON cadastros(prioritario);

-- Índices na tabela membros_familia
CREATE INDEX IF NOT EXISTS idx_membros_ref ON membros_familia(ref_id);
CREATE INDEX IF NOT EXISTS idx_membros_nome ON membros_familia(nome);

-- =====================================================
-- 4. TRIGGER PARA ATUALIZAR updated_at
-- =====================================================

-- Função para atualizar o timestamp
CREATE OR REPLACE FUNCTION atualizar_updated_at()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = TIMEZONE('utc', NOW());
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Trigger na tabela cadastros
DROP TRIGGER IF EXISTS trigger_updated_at_cadastros ON cadastros;
CREATE TRIGGER trigger_updated_at_cadastros
    BEFORE UPDATE ON cadastros
    FOR EACH ROW
    EXECUTE FUNCTION atualizar_updated_at();

-- =====================================================
-- 5. POLÍTICAS DE SEGURANÇA (RLS - Row Level Security)
-- =====================================================

-- Habilitar RLS nas tabelas
ALTER TABLE cadastros ENABLE ROW LEVEL SECURITY;
ALTER TABLE membros_familia ENABLE ROW LEVEL SECURITY;

-- Política para permitir todas as operações (modo desenvolvimento)
-- Em produção, você deve criar políticas mais restritivas

-- Política para cadastros - leitura
DROP POLICY IF EXISTS "Acesso total a cadastros" ON cadastros;
CREATE POLICY "Acesso total a cadastros" ON cadastros
    FOR ALL
    USING (true)
    WITH CHECK (true);

-- Política para membros_familia - leitura
DROP POLICY IF EXISTS "Acesso total a membros_familia" ON membros_familia;
CREATE POLICY "Acesso total a membros_familia" ON membros_familia
    FOR ALL
    USING (true)
    WITH CHECK (true);

-- =====================================================
-- 6. DADOS DE EXEMPLO (OPCIONAL)
-- =====================================================

-- Descomente as linhas abaixo se quiser inserir dados de exemplo

/*
INSERT INTO cadastros (ref_id, nome, data_ref, cpf, rg, nis, endereco, numero, bairro, cep, telefone, email, data_nascimento, prioritario)
VALUES 
    (1, 'MARIA DA SILVA', '21/03/2026 10:30', '123.456.789-00', '12.345.678-9', '123.45678.90-1', 'Rua das Flores', '100', 'Centro', '01234-567', '(11) 98765-4321', 'maria@email.com', '15/05/1980', false),
    (2, 'JOÃO SANTOS', '21/03/2026 11:00', '234.567.890-11', '23.456.789-0', '234.56789.01-2', 'Av. Principal', '500', 'Jardim das Palmeiras', '01234-568', '(11) 97654-3210', 'joao@email.com', '20/08/1975', true);

INSERT INTO membros_familia (ref_id, nome, data_nascimento, vinculo, titular)
VALUES 
    (1, 'MARIA DA SILVA', '15/05/1980', 'Titular', true),
    (1, 'JOSÉ DA SILVA', '10/03/1978', 'Cônjuge', false),
    (1, 'ANA DA SILVA', '05/12/2010', 'Filho(a)', false),
    (2, 'JOÃO SANTOS', '20/08/1975', 'Titular', true);
*/

-- =====================================================
-- FIM DO SCRIPT
-- =====================================================
