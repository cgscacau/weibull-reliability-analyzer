"""
Módulo para upload e leitura de arquivos
"""
import streamlit as st
import pandas as pd
import io
from typing import Optional, Tuple
import PyPDF2
import pdfplumber
import tabula

from config import SUPPORTED_FORMATS, ERROR_MESSAGES, SUCCESS_MESSAGES
from utils.helpers import create_info_box


class FileUploader:
    """Classe para gerenciar upload de arquivos"""
    
    def __init__(self):
        self.supported_extensions = self._get_all_extensions()
    
    def _get_all_extensions(self) -> list:
        """Retorna lista de todas as extensões suportadas"""
        extensions = []
        for format_list in SUPPORTED_FORMATS.values():
            extensions.extend(format_list)
        return extensions
    
    def upload_file(self) -> Optional[Tuple[pd.DataFrame, str]]:
        """
        Exibe widget de upload e processa o arquivo
        
        Returns:
            Tupla (DataFrame, nome_arquivo) ou None
        """
        st.subheader("📁 Upload de Dados")
        
        # Informações sobre formatos suportados
        with st.expander("ℹ️ Formatos Suportados", expanded=False):
            st.markdown("""
            **Formatos aceitos:**
            - **CSV** (.csv): Arquivo de texto separado por vírgulas ou ponto-e-vírgula
            - **Excel** (.xlsx, .xls): Planilhas do Microsoft Excel
            - **PDF** (.pdf): Tabelas extraídas de documentos PDF
            
            **Dica:** Para melhores resultados, use arquivos CSV ou Excel.
            """)
        
        uploaded_file = st.file_uploader(
            "Escolha um arquivo",
            type=self.supported_extensions,
            help="Arraste e solte ou clique para selecionar um arquivo"
        )
        
        if uploaded_file is not None:
            try:
                # Determina o tipo de arquivo
                file_extension = uploaded_file.name.split('.')[-1].lower()
                
                # Processa o arquivo baseado na extensão
                if file_extension == 'csv':
                    df = self._read_csv(uploaded_file)
                elif file_extension in ['xlsx', 'xls']:
                    df = self._read_excel(uploaded_file)
                elif file_extension == 'pdf':
                    df = self._read_pdf(uploaded_file)
                else:
                    create_info_box(ERROR_MESSAGES["INVALID_FORMAT"], "error")
                    return None
                
                if df is not None and not df.empty:
                    create_info_box(SUCCESS_MESSAGES["FILE_LOADED"], "success")
                    
                    # Exibe preview dos dados
                    with st.expander("👁️ Visualizar Dados", expanded=True):
                        st.dataframe(df.head(10), use_container_width=True)
                        st.caption(f"Mostrando 10 de {len(df)} linhas")
                    
                    return df, uploaded_file.name
                else:
                    create_info_box("❌ Arquivo vazio ou não pôde ser lido.", "error")
                    return None
                    
            except Exception as e:
                create_info_box(f"❌ Erro ao processar arquivo: {str(e)}", "error")
                return None
        
        return None
    
    def _read_csv(self, file) -> Optional[pd.DataFrame]:
        """
        Lê arquivo CSV
        
        Args:
            file: Arquivo uploaded
        
        Returns:
            DataFrame ou None
        """
        try:
            # Tenta diferentes separadores
            for sep in [',', ';', '\t', '|']:
                try:
                    file.seek(0)
                    df = pd.read_csv(file, sep=sep, encoding='utf-8')
                    if len(df.columns) > 1:  # Sucesso se tiver mais de uma coluna
                        return df
                except:
                    continue
            
            # Se nenhum separador funcionou, tenta com encoding diferente
            file.seek(0)
            df = pd.read_csv(file, sep=None, engine='python', encoding='latin-1')
            return df
            
        except Exception as e:
            st.error(f"Erro ao ler CSV: {str(e)}")
            return None
    
    def _read_excel(self, file) -> Optional[pd.DataFrame]:
        """
        Lê arquivo Excel
        
        Args:
            file: Arquivo uploaded
        
        Returns:
            DataFrame ou None
        """
        try:
            # Lê a primeira planilha
            df = pd.read_excel(file, sheet_name=0)
            
            # Se houver múltiplas planilhas, permite seleção
            excel_file = pd.ExcelFile(file)
            if len(excel_file.sheet_names) > 1:
                sheet_name = st.selectbox(
                    "Selecione a planilha:",
                    excel_file.sheet_names
                )
                df = pd.read_excel(file, sheet_name=sheet_name)
            
            return df
            
        except Exception as e:
            st.error(f"Erro ao ler Excel: {str(e)}")
            return None
    
    def _read_pdf(self, file) -> Optional[pd.DataFrame]:
        """
        Lê tabelas de arquivo PDF
        
        Args:
            file: Arquivo uploaded
        
        Returns:
            DataFrame ou None
        """
        try:
            # Salva o arquivo temporariamente
            with open("temp.pdf", "wb") as f:
                f.write(file.getbuffer())
            
            # Tenta extrair tabelas com tabula
            try:
                tables = tabula.read_pdf("temp.pdf", pages='all', multiple_tables=True)
                if tables:
                    if len(tables) > 1:
                        st.warning(f"⚠️ {len(tables)} tabelas encontradas. Usando a primeira.")
                    df = tables[0]
                    return df
            except:
                pass
            
            # Se tabula falhar, tenta com pdfplumber
            with pdfplumber.open("temp.pdf") as pdf:
                all_tables = []
                for page in pdf.pages:
                    tables = page.extract_tables()
                    all_tables.extend(tables)
                
                if all_tables:
                    # Converte primeira tabela para DataFrame
                    table = all_tables[0]
                    df = pd.DataFrame(table[1:], columns=table[0])
                    return df
            
            st.error("Nenhuma tabela encontrada no PDF.")
            return None
            
        except Exception as e:
            st.error(f"Erro ao ler PDF: {str(e)}")
            return None
        finally:
            # Remove arquivo temporário
            import os
            if os.path.exists("temp.pdf"):
                os.remove("temp.pdf")
