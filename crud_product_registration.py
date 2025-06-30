import streamlit as st

# Inicialização de estados
if "produtos" not in st.session_state:
    st.session_state.produtos = []

if "indice_edicao_produto" not in st.session_state:
    st.session_state.indice_edicao_produto = None

if "indice_exclusao_produto" not in st.session_state:
    st.session_state.indice_exclusao_produto = None

if "indice_visualizacao_produto" not in st.session_state:
    st.session_state.indice_visualizacao_produto = None

if "pagina_atual" not in st.session_state:
    st.session_state.pagina_atual = "Produtos"


def formatar_moeda(valor):
    """Formatar como moeda brasileira"""
    return (
        f"R$ {valor:,.2f}".replace(",", "X")
        .replace(".", ",")
        .replace("X", ".")
    )


# Menu lateral com botão ocupando 100% da largura
st.sidebar.title("Menu")
if st.sidebar.button("📋 Produtos", use_container_width=True):
    st.session_state.pagina_atual = "Produtos"
    st.rerun()

pagina = st.session_state.pagina_atual

st.title("📦 Sistema de Gestão")

# =========================
# Página: Lista de Produtos
# =========================
if pagina == "Produtos":
    st.subheader("📋 Lista de Produtos")

    st.button(
        "➕ Novo Produto",
        on_click=lambda: st.session_state.update(
            pagina_atual="Adicionar Produto"
        ),
    )

    st.markdown("---")

    if not st.session_state.produtos:
        st.info("Nenhum produto adicionado ainda.")
    else:
        for indice, produto in enumerate(st.session_state.produtos):
            col1, col2 = st.columns([3, 4])
            with col1:
                st.markdown(
                    f"**{produto['nome']}** — "
                    f"{formatar_moeda(produto['preco'])}"
                )
            with col2:
                col_vis, col_edi, col_del = st.columns(3)
                with col_vis:
                    if st.button(
                        "👁️ Visualizar",
                        key=f"visualizar_{indice}",
                        use_container_width=True,
                    ):
                        st.session_state.indice_visualizacao_produto = indice
                        st.session_state.pagina_atual = "Visualizar Produto"
                        st.rerun()
                with col_edi:
                    if st.button(
                        "✏️ Editar",
                        key=f"editar_{indice}",
                        use_container_width=True,
                    ):
                        st.session_state.indice_edicao_produto = indice
                        st.session_state.pagina_atual = "Editar Produto"
                        st.rerun()
                with col_del:
                    if st.button(
                        "🗑️ Excluir",
                        key=f"excluir_{indice}",
                        use_container_width=True,
                    ):
                        st.session_state.indice_exclusao_produto = indice
                        st.session_state.pagina_atual = "Excluir Produto"
                        st.rerun()

# =========================
# Página: Adicionar Produto
# =========================
elif pagina == "Adicionar Produto":
    st.subheader("➕ Adicionar Novo Produto")
    with st.form("form_adicionar"):
        nome = st.text_input("Nome do Produto")
        preco = st.number_input(
            "Preço (R$)", min_value=0.0, step=0.01, format="%.2f"
        )
        col_ad, col_can = st.columns(2)
        with col_ad:
            adicionar = st.form_submit_button("Adicionar")
        with col_can:
            cancelar = st.form_submit_button("Cancelar")
        if adicionar:
            if nome:
                st.session_state.produtos.append(
                    {"nome": nome, "preco": preco}
                )
                st.success(f"Produto '{nome}' adicionado com sucesso!")
                st.session_state.pagina_atual = "Produtos"
                st.rerun()
            else:
                st.warning("Por favor, insira o nome do produto.")
        elif cancelar:
            st.session_state.pagina_atual = "Produtos"
            st.rerun()

# =========================
# Página: Editar Produto
# =========================
elif pagina == "Editar Produto":
    indice = st.session_state.indice_edicao_produto
    if indice is not None and indice < len(st.session_state.produtos):
        produto = st.session_state.produtos[indice]
        st.subheader("✏️ Editar Produto")
        with st.form("form_editar"):
            novo_nome = st.text_input("Nome do Produto", value=produto["nome"])
            novo_preco = st.number_input(
                "Preço (R$)",
                value=produto["preco"],
                min_value=0.0,
                step=0.01,
                format="%.2f",
            )
            col_salvar, col_cancelar = st.columns(2)
            with col_salvar:
                salvar = st.form_submit_button(
                    "Salvar", use_container_width=True
                )
            with col_cancelar:
                cancelar = st.form_submit_button(
                    "Cancelar", use_container_width=True
                )
            if salvar:
                st.session_state.produtos[indice]["nome"] = novo_nome
                st.session_state.produtos[indice]["preco"] = novo_preco
                st.success("Produto atualizado com sucesso!")
                st.session_state.indice_edicao_produto = None
                st.session_state.pagina_atual = "Produtos"
                st.rerun()
            elif cancelar:
                st.session_state.indice_edicao_produto = None
                st.session_state.pagina_atual = "Produtos"
                st.rerun()
    else:
        st.error("Produto não encontrado.")
        st.session_state.indice_edicao_produto = None
        st.session_state.pagina_atual = "Produtos"
        st.rerun()

# =========================
# Página: Visualizar Produto
# =========================
elif pagina == "Visualizar Produto":
    indice = st.session_state.indice_visualizacao_produto
    if indice is not None and indice < len(st.session_state.produtos):
        produto = st.session_state.produtos[indice]
        st.subheader("👁️ Detalhes do Produto")
        st.markdown(f"**Nome:** {produto['nome']}")
        st.markdown(f"**Preço:** {formatar_moeda(produto['preco'])}")
        if st.button("🔙 Voltar"):
            st.session_state.indice_visualizacao_produto = None
            st.session_state.pagina_atual = "Produtos"
            st.rerun()
    else:
        st.error("Produto não encontrado.")
        st.session_state.indice_visualizacao_produto = None
        st.session_state.pagina_atual = "Produtos"
        st.rerun()

# =========================
# Página: Excluir Produto
# =========================
elif pagina == "Excluir Produto":
    st.subheader("⚠️ Confirmar Exclusão de Produto")
    st.divider()

    indice = st.session_state.indice_exclusao_produto
    if indice is not None and indice < len(st.session_state.produtos):
        produto = st.session_state.produtos[indice]
        st.warning(
            f"Tem certeza que deseja excluir o "
            f"produto **'{produto['nome']}'**? "
            f"Esta ação é **irreversível**."
        )

        col_conf, col_canc_exc = st.columns(2)
        with col_conf:
            if st.button(
                "✅ **Sim**",
                use_container_width=True,
                type="primary",
            ):
                del st.session_state.produtos[indice]
                st.success(
                    f"Produto '**{produto['nome']}**' excluído com sucesso!"
                )
                st.session_state.produto_a_excluir_indice = None
                st.session_state.pagina_atual = "Produtos"
                st.rerun()
        with col_canc_exc:
            if st.button("❌ Cancelar", use_container_width=True):
                st.session_state.produto_a_excluir_indice = None
                st.session_state.pagina_atual = "Produtos"
                st.rerun()
    else:
        st.error("Produto para exclusão não encontrado.")
        st.session_state.produto_a_excluir_indice = None
        st.session_state.pagina_atual = "Produtos"
        st.rerun()
