from supabase import create_client, Client
from config import Config
from datetime import datetime


class SupabaseDB:
    """Gerenciador de conexão e operações com Supabase"""
    
    def __init__(self):
        self.client: Client = None
        self._conectar()
    
    def _conectar(self):
        """Estabelece conexão com Supabase"""
        try:
            self.client = create_client(
                Config.SUPABASE_URL,
                Config.SUPABASE_KEY
            )
            print("✓ Conexão com Supabase estabelecida com sucesso!")
        except Exception as e:
            print(f"✗ Erro ao conectar com Supabase: {e}")
            self.client = None
    
    def testar_conexao(self):
        """Testa a conexão com Supabase"""
        if not self.client:
            return False, "Cliente não inicializado"
        
        try:
            # Tentar buscar um registro da tabela cadastros
            response = self.client.table("cadastros").select("ref_id").limit(1).execute()
            return True, "Conexão OK"
        except Exception as e:
            return False, str(e)
    
    # ========== OPERAÇÕES COM USUÁRIOS ==========

    def buscar_usuario_por_email(self, email):
        """Busca usuário por e-mail para login"""
        try:
            response = self.client.table("usuarios")\
                .select("*")\
                .eq("email", email)\
                .execute()
            
            if response.data and len(response.data) > 0:
                return response.data[0]
            
            return None
        except Exception as e:
            print(f"✗ Erro ao buscar usuário: {e}")
            return None

    def inserir_usuario(self, nome, email, senha_hash):
        """Insere um novo usuário administrativo"""
        try:
            dados = {
                'nome': nome,
                'email': email,
                'senha_hash': senha_hash
            }
            response = self.client.table("usuarios").insert(dados).execute()
            return True if response.data else False
        except Exception as e:
            print(f"✗ Erro ao inserir usuário: {e}")
            return False

    # ========== OPERAÇÕES COM CADASTROS ==========
    
    def obter_proximo_ref(self):
        """Obtém o próximo número de referência"""
        try:
            response = self.client.table("cadastros").select("ref_id").order("ref_id", desc=True).limit(1).execute()
            
            if response.data and len(response.data) > 0:
                ultimo_ref = response.data[0]['ref_id']
                return ultimo_ref + 1
            
            return 1  # Primeiro cadastro
        except Exception as e:
            print(f"Erro ao obter próximo REF: {e}")
            return 1
    
    def inserir_cadastro(self, dados):
        """Insere novo cadastro"""
        try:
            # Obter próximo REF
            ref_id = self.obter_proximo_ref()
            
            # Adicionar REF e data
            dados['ref_id'] = ref_id
            dados['data_ref'] = datetime.now().strftime('%d/%m/%Y %H:%M')
            
            # Inserir no Supabase
            response = self.client.table("cadastros").insert(dados).execute()
            
            if response.data:
                print(f"✓ Cadastro REF {ref_id} inserido com sucesso!")
                return ref_id, True
            
            return None, False
            
        except Exception as e:
            print(f"✗ Erro ao inserir cadastro: {e}")
            return None, False
    
    def atualizar_cadastro(self, ref_id, dados):
        """Atualiza cadastro existente"""
        try:
            response = self.client.table("cadastros")\
                .update(dados)\
                .eq("ref_id", ref_id)\
                .execute()
            
            if response.data:
                print(f"✓ Cadastro REF {ref_id} atualizado com sucesso!")
                return True
            
            return False
            
        except Exception as e:
            print(f"✗ Erro ao atualizar cadastro: {e}")
            return False
    
    def buscar_cadastro(self, ref_id):
        """Busca cadastro por REF"""
        try:
            response = self.client.table("cadastros")\
                .select("*")\
                .eq("ref_id", ref_id)\
                .execute()
            
            if response.data and len(response.data) > 0:
                return response.data[0]
            
            return None
            
        except Exception as e:
            print(f"✗ Erro ao buscar cadastro: {e}")
            return None
    
    def buscar_cadastros(self, termo=None):
        """Busca cadastros por termo ou retorna todos"""
        try:
            query = self.client.table("cadastros").select("*")
            
            if termo:
                termo_lower = termo.lower()
                # Busca por nome, CPF, NIS ou REF
                response = query.execute()
                
                if response.data:
                    resultados = []
                    for cadastro in response.data:
                        if (termo_lower in str(cadastro.get('nome', '')).lower() or
                            termo_lower in str(cadastro.get('cpf', '')).lower() or
                            termo_lower in str(cadastro.get('nis', '')).lower() or
                            termo_lower in str(cadastro.get('ref_id', '')).lower()):
                            resultados.append(cadastro)
                    return resultados
            
            else:
                response = query.order("ref_id", desc=True).execute()
            
            return response.data if response.data else []
            
        except Exception as e:
            print(f"✗ Erro ao buscar cadastros: {e}")
            return []
    
    def excluir_cadastro(self, ref_id):
        """Exclui cadastro (e membros em cascata)"""
        try:
            response = self.client.table("cadastros")\
                .delete()\
                .eq("ref_id", ref_id)\
                .execute()
            
            print(f"✓ Cadastro REF {ref_id} excluído com sucesso!")
            return True
            
        except Exception as e:
            print(f"✗ Erro ao excluir cadastro: {e}")
            return False
    
    # ========== OPERAÇÕES COM MEMBROS DA FAMÍLIA ==========
    
    def adicionar_membro_familia(self, ref_id, nome, data_nascimento, vinculo, titular):
        """Adiciona membro à família"""
        try:
            membro = {
                'ref_id': ref_id,
                'nome': nome,
                'data_nascimento': data_nascimento,
                'vinculo': vinculo,
                'titular': titular
            }
            
            response = self.client.table("membros_familia").insert(membro).execute()
            
            if response.data:
                print(f"✓ Membro '{nome}' adicionado à família REF {ref_id}")
                return True
            
            return False
            
        except Exception as e:
            print(f"✗ Erro ao adicionar membro da família: {e}")
            return False
    
    def obter_membros_familia(self, ref_id):
        """Obtém todos os membros da família"""
        try:
            response = self.client.table("membros_familia")\
                .select("*")\
                .eq("ref_id", ref_id)\
                .execute()
            
            return response.data if response.data else []
            
        except Exception as e:
            print(f"✗ Erro ao obter membros da família: {e}")
            return []
    
    def remover_membro_familia(self, membro_id):
        """Remove membro da família"""
        try:
            response = self.client.table("membros_familia")\
                .delete()\
                .eq("id", membro_id)\
                .execute()
            
            print(f"✓ Membro ID {membro_id} removido com sucesso!")
            return True
            
        except Exception as e:
            print(f"✗ Erro ao remover membro da família: {e}")
            return False
    
    def buscar_por_membro_familia(self, nome_membro):
        """Busca cadastros por nome de membro da família"""
        try:
            # Primeiro busca os membros
            response_membros = self.client.table("membros_familia")\
                .select("ref_id")\
                .ilike("nome", f"%{nome_membro}%")\
                .execute()
            
            if response_membros.data:
                refs = [m['ref_id'] for m in response_membros.data]
                
                # Agora busca os cadastros com esses refs
                response_cadastros = self.client.table("cadastros")\
                    .select("*")\
                    .in_("ref_id", refs)\
                    .execute()
                
                return response_cadastros.data if response_cadastros.data else []
            
            return []
            
        except Exception as e:
            print(f"✗ Erro ao buscar por membro da família: {e}")
            return []

    # ========== OPERAÇÕES COM PRONTUÁRIOS ==========
    
    def criar_prontuario(self, dados):
        try:
            response = self.client.table("prontuarios").insert(dados).execute()
            if response.data:
                return response.data[0]['id'], True
            return None, False
        except Exception as e:
            print(f"✗ Erro ao criar prontuário: {e}")
            return None, False
            
    def buscar_prontuario_por_cadastro(self, cadastro_ref_id):
        try:
            response = self.client.table("prontuarios")\
                .select("*, usuarios(nome)")\
                .eq("cadastro_ref_id", cadastro_ref_id)\
                .execute()
                
            if response.data and len(response.data) > 0:
                return response.data[0]
            return None
        except Exception as e:
            print(f"✗ Erro ao buscar prontuário por ref: {e}")
            return None
            
    def buscar_prontuario(self, prontuario_id):
        try:
            response = self.client.table("prontuarios")\
                .select("*, usuarios(nome)")\
                .eq("id", prontuario_id)\
                .execute()
                
            if response.data and len(response.data) > 0:
                return response.data[0]
            return None
        except Exception as e:
            print(f"✗ Erro ao buscar prontuário: {e}")
            return None

    # ========== OPERAÇÕES COM ATENDIMENTOS ==========
    
    def registrar_atendimento(self, dados):
        try:
            response = self.client.table("atendimentos").insert(dados).execute()
            if response.data:
                return response.data[0]['id'], True
            return None, False
        except Exception as e:
            print(f"✗ Erro ao registrar atendimento: {e}")
            return None, False

    def obter_atendimentos_do_prontuario(self, prontuario_id):
        try:
            response = self.client.table("atendimentos")\
                .select("*, usuarios(nome)")\
                .eq("prontuario_id", prontuario_id)\
                .order("data_atendimento", desc=True)\
                .execute()
                
            return response.data if response.data else []
        except Exception as e:
            print(f"✗ Erro ao obter atendimentos: {e}")
            return []
            
    def buscar_atendimento(self, atendimento_id):
        try:
            response = self.client.table("atendimentos")\
                .select("*, usuarios(nome)")\
                .eq("id", atendimento_id)\
                .execute()
                
            if response.data and len(response.data) > 0:
                return response.data[0]
            return None
        except Exception as e:
            print(f"✗ Erro ao buscar atendimento: {e}")
            return None

    # ========== OPERAÇÕES COM ENCAMINHAMENTOS ==========
    
    def registrar_encaminhamento(self, dados):
        try:
            response = self.client.table("encaminhamentos").insert(dados).execute()
            if response.data:
                return response.data[0]['id'], True
            return None, False
        except Exception as e:
            print(f"✗ Erro ao registrar encaminhamento: {e}")
            return None, False

    def buscar_encaminhamento(self, enc_id):
        try:
            response = self.client.table("encaminhamentos").select("*").eq("id", enc_id).execute()
            if response.data and len(response.data) > 0:
                return response.data[0]
            return None
        except Exception as e:
            print(f"✗ Erro ao buscar encaminhamento: {e}")
            return None
            
    def concluir_encaminhamento(self, enc_id):
        try:
            response = self.client.table("encaminhamentos").update({"status": "Realizado"}).eq("id", enc_id).execute()
            if response.data:
                return True
            return False
        except Exception as e:
            print(f"✗ Erro ao concluir encaminhamento: {e}")
            return False

    def obter_encaminhamentos_do_atendimento(self, atendimento_id):
        try:
            response = self.client.table("encaminhamentos")\
                .select("*")\
                .eq("atendimento_id", atendimento_id)\
                .order("created_at", desc=False)\
                .execute()
                
            return response.data if response.data else []
        except Exception as e:
            print(f"✗ Erro ao obter encaminhamentos do atendimento: {e}")
            return []
            
    def obter_encaminhamentos_do_prontuario(self, prontuario_id):
        try:
            atendimentos = self.obter_atendimentos_do_prontuario(prontuario_id)
            if not atendimentos:
                return []
                
            ids_atendimentos = [a['id'] for a in atendimentos]
            
            response = self.client.table("encaminhamentos")\
                .select("*")\
                .in_("atendimento_id", ids_atendimentos)\
                .order("created_at", desc=True)\
                .execute()
            
            return response.data if response.data else []
        except Exception as e:
            print(f"✗ Erro ao obter todos os encaminhamentos do prontuário: {e}")
            return []


# Instância singleton do banco de dados
db = SupabaseDB()
